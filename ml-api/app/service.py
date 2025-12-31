import os
import joblib
import pandas as pd
import numpy as np
import duckdb
from mappings import mapa_escolaridade, mapa_tamanho, mapa_setor, mapa_sexo, mapa_raca

class SalarioService:
    def __init__(self):
        # Variáveis de Estado
        self.modelo = None
        self.encoders = None
        self.cbo_map = None
        self.mapa_medias = None
        self.media_global = None
        self.nome_para_cbo = None
        
        # Substitui o self.df_rais (memória) pelo caminho do arquivo (disco)
        self.caminho_parquet = None 
        
        # O MAPA DE FALLBACK AGORA É CALCULADO NO STARTUP
        self.mapa_fallback = {} 

        # Sequência de Inicialização (Nomes originais mantidos)
        self._carregar_modelo()
        self._carregar_dados_rais()

    def _carregar_modelo(self):
        """Carrega o modelo de ML treinado e seus artefatos."""
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_base, 'modelo_salario_ti.pkl')
        
        try:
            pacote = joblib.load(caminho_arquivo)
            self.modelo = pacote['modelo']
            self.encoders = pacote['encoders']
            self.cbo_map = pacote['cbo_map']
            self.mapa_medias = pacote.get('mapa_medias', {})
            self.media_global = pacote.get('media_global', 3000.0)
            
            self.nome_para_cbo = {str(v).strip(): str(k) for k, v in self.cbo_map.items()}
            print("[OK] Modelo ML carregado com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Falha crítica ao carregar modelo: {e}")

    def _carregar_dados_rais(self):
        """
        Nome antigo mantido.
        Mas em vez de carregar Pandas na RAM, apenas localiza o arquivo para o DuckDB.
        """
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        
        # TENTA ACHAR O ARQUIVO CORRETO (Prioridade para o arquivo de TCC/Amostra)
        opcoes = ['dados_rais_amostra.parquet', 'dados_rais_lite.parquet', 'dados_rais_tcc.parquet']
        self.caminho_parquet = None

        for nome in opcoes:
            caminho = os.path.join(diretorio_base, nome)
            if os.path.exists(caminho):
                self.caminho_parquet = caminho
                break
        
        if self.caminho_parquet:
            print(f"[INIT] Parquet encontrado para DuckDB: {self.caminho_parquet}")
            self._calcular_quartis_globais()
        else:
            print("[CRITICAL WARN] NENHUM Arquivo Parquet encontrado! O Mapa virá vazio.")
            self.mapa_fallback = {"JUNIOR": 25, "PLENO": 30, "SENIOR": 38, "ESPECIALISTA": 45}

    def _calcular_quartis_globais(self):
        """Calcula quartis globais via SQL direto no disco."""
        try:
            query = f"""
                SELECT 
                    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY idade) as q25,
                    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY idade) as q50,
                    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY idade) as q75,
                    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY idade) as q90
                FROM '{self.caminho_parquet}'
                WHERE idade BETWEEN 18 AND 80
            """
            resultado = duckdb.sql(query).fetchone()
            
            if resultado:
                self.mapa_fallback = {
                    "JUNIOR": int(resultado[0]),
                    "PLENO": int(resultado[1]),
                    "SENIOR": int(resultado[2]),
                    "ESPECIALISTA": int(resultado[3])
                }
                print(f"[STATS] Quartis Globais (DuckDB): {self.mapa_fallback}")
            else:
                raise ValueError("Query retornou vazio")

        except Exception as e:
            print(f"[WARN] Erro ao calcular stats globais: {e}. Usando padrão.")
            self.mapa_fallback = {"JUNIOR": 27, "PLENO": 32, "SENIOR": 40, "ESPECIALISTA": 47}

    def _resolver_idade(self, cargo_nome, ano, idade_manual, faixa_experiencia):
        """Lógica de Idade via DuckDB (Filtra Cargo + Ano no disco)."""
        if faixa_experiencia is None:
            return idade_manual if idade_manual is not None else self.mapa_fallback.get("PLENO", 32)

        cbo_codigo = self.nome_para_cbo.get(cargo_nome)
        
        if cbo_codigo and self.caminho_parquet and os.path.exists(self.caminho_parquet):
            cbo_limpo = str(cbo_codigo).replace('-', '').strip()
            
            try:
                # Query com filtro de ANO
                query = f"""
                    SELECT 
                        COUNT(*) as total,
                        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY idade) as q25,
                        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY idade) as q50,
                        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY idade) as q75,
                        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY idade) as q90
                    FROM '{self.caminho_parquet}'
                    WHERE replace(CAST(cbo_2002 AS VARCHAR), '-', '') = '{cbo_limpo}'
                      AND ano = {ano}
                """
                res = duckdb.sql(query).fetchone()
                
                # Se tiver amostra relevante (> 50), usa a estatística específica
                if res and res[0] >= 50:
                    match faixa_experiencia:
                        case "JUNIOR": return int(res[1])
                        case "PLENO": return int(res[2])
                        case "SENIOR": return int(res[3])
                        case "ESPECIALISTA": return int(res[4])
            except Exception as e:
                print(f"[ERROR] Erro DuckDB resolver idade: {e}")

        # Fallback
        return self.mapa_fallback.get(faixa_experiencia, 32)

    def prever(self, dados):
        """Endpoint Individual (/predict)"""
        idade_calculada = self._resolver_idade(
            dados.cargo.value, dados.ano, dados.idade, dados.faixa_experiencia
        )

        cbo_codigo = self.nome_para_cbo.get(dados.cargo.value, "000000")
        cod_tamanho = mapa_tamanho.get(dados.tamanho_empresa.value, 6)
        cod_escolaridade = mapa_escolaridade.get(dados.escolaridade.value, 9)
        cod_setor = mapa_setor.get(dados.setor.value, 18)
        cod_sexo_rais = 1 if dados.sexo.value == "Masculino" else 2 
        cod_raca_rais = mapa_raca.get(dados.raca.value, 9)

        # Target Encoding (Vem do Pickle, rápido)
        val_cbo = self.mapa_medias['cbo'].get(str(cbo_codigo), self.media_global)
        val_esc = self.mapa_medias['esc'].get(str(cod_escolaridade), self.media_global)
        val_uf = self.mapa_medias['uf'].get(dados.uf.upper(), self.media_global)
        val_tam = self.mapa_medias['tam'].get(str(cod_tamanho), self.media_global)
        val_setor = self.mapa_medias['setor'].get(str(cod_setor), self.media_global)

        try:
            val_sexo_encoded = self.encoders['sexo'].transform([str(cod_sexo_rais)])[0]
            val_raca_encoded = self.encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
        except:
            val_sexo_encoded, val_raca_encoded = 0, 0

        df_input = pd.DataFrame({
            'cbo_valor': [val_cbo],
            'idade': [idade_calculada],
            'esc_valor': [val_esc],
            'uf_valor': [val_uf],
            'tam_valor': [val_tam],
            'setor_valor': [val_setor],
            'sexo': [val_sexo_encoded],
            'raca_cor_valor': [val_raca_encoded],
            'ano': [dados.ano]
        })

        log_salario = self.modelo.predict(df_input)[0]
        return float(np.expm1(log_salario))

    def gerar_dados_mapa(self, dados_solicitacao):
        """Endpoint Batch (/analise/mapa) via DuckDB"""
        estados_br = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
            'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]

        print(f"[MAPA] Iniciando para Cargo: {dados_solicitacao.cargo.value}, Ano: {dados_solicitacao.ano}")

        cbo_codigo = self.nome_para_cbo.get(dados_solicitacao.cargo.value)
        if not cbo_codigo:
            print(f"[ERROR] Cargo '{dados_solicitacao.cargo.value}' não encontrado no CBO MAP!")
            cbo_codigo = "000000"

        idade_calculada = self._resolver_idade(
            dados_solicitacao.cargo.value, dados_solicitacao.ano, 
            dados_solicitacao.idade, dados_solicitacao.faixa_experiencia
        )

        stats_por_uf = {}
        # Só executa SQL se o arquivo existir e tivermos CBO válido
        if cbo_codigo != "000000" and self.caminho_parquet and os.path.exists(self.caminho_parquet):
            cbo_limpo = str(cbo_codigo).replace('-', '').strip()
            
            try:
                # Query Agregada DuckDB com FILTRO DE ANO
                query = f"""
                    SELECT sigla_uf, sexo, COUNT(*) as qtd
                    FROM '{self.caminho_parquet}'
                    WHERE replace(CAST(cbo_2002 AS VARCHAR), '-', '') = '{cbo_limpo}'
                      AND ano = {dados_solicitacao.ano}  -- <--- FILTRO DE ANO OBRIGATÓRIO
                    GROUP BY sigla_uf, sexo
                """
                resultados = duckdb.sql(query).fetchall()
                
                # Processa o resultado do SQL
                for linha in resultados:
                    uf = linha[0]
                    sexo = linha[1] # 1=Masc, 2=Fem
                    qtd = linha[2]
                    
                    if uf not in stats_por_uf:
                        stats_por_uf[uf] = {'total': 0, 'masculino': 0, 'feminino': 0}
                    
                    stats_por_uf[uf]['total'] += qtd
                    if sexo == 1:
                        stats_por_uf[uf]['masculino'] += qtd
                    elif sexo == 2:
                        stats_por_uf[uf]['feminino'] += qtd
                
                print(f"[MAPA] Dados encontrados para {len(stats_por_uf)} estados.")

            except Exception as e:
                print(f"[ERROR] Erro DuckDB mapa: {e}")

        # Daqui para baixo é igual ao antigo (preparação do batch para o modelo)
        cod_tamanho = mapa_tamanho.get(dados_solicitacao.tamanho_empresa.value, 6)
        cod_escolaridade = mapa_escolaridade.get(dados_solicitacao.escolaridade.value, 9)
        cod_setor = mapa_setor.get(dados_solicitacao.setor.value, 17)
        cod_sexo_rais = 1 
        cod_raca_rais = 2

        val_cbo = self.mapa_medias['cbo'].get(str(cbo_codigo), self.media_global)
        val_esc = self.mapa_medias['esc'].get(str(cod_escolaridade), self.media_global)
        val_tam = self.mapa_medias['tam'].get(str(cod_tamanho), self.media_global)
        val_setor = self.mapa_medias['setor'].get(str(cod_setor), self.media_global)

        try:
            val_sexo_encoded = self.encoders['sexo'].transform([str(cod_sexo_rais)])[0]
            val_raca_encoded = self.encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
        except:
            val_sexo_encoded, val_raca_encoded = 0, 0

        input_batch = []
        for uf in estados_br:
            val_uf = self.mapa_medias['uf'].get(uf, self.media_global)
            input_batch.append({
                'cbo_valor': val_cbo,
                'idade': idade_calculada,
                'esc_valor': val_esc,
                'uf_valor': val_uf,
                'tam_valor': val_tam,
                'setor_valor': val_setor,
                'sexo': val_sexo_encoded,
                'raca_cor_valor': val_raca_encoded,
                'ano': dados_solicitacao.ano
            })

        df_batch = pd.DataFrame(input_batch)
        try:
            log_salarios = self.modelo.predict(df_batch)
            salarios_reais = np.expm1(log_salarios)
        except Exception as e:
            print(f"[ERROR] Falha no predict do modelo: {e}")
            salarios_reais = [0] * 27

        resultado = []
        for i, uf in enumerate(estados_br):
            stats = stats_por_uf.get(uf, {'total': 0, 'masculino': 0, 'feminino': 0})
            resultado.append({
                "uf": f"br-{uf.lower()}",
                "salario_estimado": round(float(salarios_reais[i]), 2),
                "quantidade_total": stats['total'],
                "quantidade_masculino": stats['masculino'],
                "quantidade_feminino": stats['feminino']
            })
            
        return resultado

salario_service = SalarioService()