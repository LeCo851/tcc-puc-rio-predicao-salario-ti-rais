import os
import joblib
import pandas as pd
import numpy as np
from mappings import mapa_escolaridade, mapa_tamanho, mapa_setor, mapa_sexo, mapa_raca

class SalarioService:
    def __init__(self):
        self.modelo = None
        self.encoders = None
        self.cbo_map = None
        self.mapa_medias = None
        self.media_global = None
        self.nome_para_cbo = None
        self.df_rais = None
        
        # Carrega tudo na inicialização
        self._carregar_modelo()
        self._carregar_dados_rais()

    def _carregar_modelo(self):
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_base, 'modelo_salario_ti.pkl')
        
        print(f"[INIT] Carregando modelo de: {caminho_arquivo}")
        try:
            pacote = joblib.load(caminho_arquivo)
            self.modelo = pacote['modelo']
            self.encoders = pacote['encoders']
            self.cbo_map = pacote['cbo_map']
            self.mapa_medias = pacote.get('mapa_medias', {})
            self.media_global = pacote.get('media_global', 3000.0)
            
            # Inverte o mapa CBO (Nome -> Código)
            self.nome_para_cbo = {str(v).strip(): str(k) for k, v in self.cbo_map.items()}
            print("[OK] Modelo carregado com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Falha crítica ao carregar modelo: {e}")

    def _carregar_dados_rais(self):
            """Carrega a base real para contagem de profissionais"""
            diretorio_base = os.path.dirname(os.path.abspath(__file__))
            caminho_parquet = os.path.join(diretorio_base, 'dados_rais_brutos.parquet')
            
            # Adicionamos 'ano' e 'sexo' nas colunas carregadas
            colunas_necessarias = ['cbo_2002', 'sigla_uf', 'ano', 'sexo']
            
            print(f"[INIT] Carregando base RAIS de: {caminho_parquet}")
            try:
                if os.path.exists(caminho_parquet):
                    self.df_rais = pd.read_parquet(caminho_parquet, columns=colunas_necessarias)
                    # Otimização: Converter para tipos leves
                    self.df_rais['cbo_2002'] = self.df_rais['cbo_2002'].astype('category')
                    self.df_rais['sigla_uf'] = self.df_rais['sigla_uf'].astype('category')
                    self.df_rais['ano'] = self.df_rais['ano'].astype('int16')
                    self.df_rais['sexo'] = self.df_rais['sexo'].astype('int8') # 1=Masc, 2=Fem
                    print(f"[OK] Base RAIS carregada: {len(self.df_rais)} registros.")
                else:
                    print("[WARN] Arquivo Parquet não encontrado. Contagens serão 0.")
                    self.df_rais = pd.DataFrame(columns=colunas_necessarias)
            except Exception as e:
                print(f"[ERROR] Erro ao ler Parquet: {e}")
                self.df_rais = pd.DataFrame(columns=colunas_necessarias)

    def prever(self, dados):
        # Lógica de previsão individual (Mantida igual)
        cbo_codigo = self.nome_para_cbo.get(dados.cargo.value, "000000")
        cod_tamanho = mapa_tamanho.get(dados.tamanho_empresa.value, 6)
        cod_escolaridade = mapa_escolaridade.get(dados.escolaridade.value, 9)
        cod_setor = mapa_setor.get(dados.setor.value, 13)
        cod_sexo_rais = mapa_sexo.get(dados.sexo.value, 1)
        cod_raca_rais = mapa_raca.get(dados.raca.value, 2)

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
            'idade': [dados.idade],
            'esc_valor': [val_esc],
            'uf_valor': [val_uf],
            'tam_valor': [val_tam],
            'setor_valor': [val_setor],
            'sexo': [val_sexo_encoded],
            'raca_cor_valor': [val_raca_encoded],
            'ano': [dados.ano_referencia]
        })

        log_salario = self.modelo.predict(df_input)[0]
        return float(np.expm1(log_salario))

    def gerar_dados_mapa(self, dados_solicitacao):
            """ 
            Gera estatísticas + previsão considerando TODOS os filtros.
            Recebe o objeto SolicitacaoMapa inteiro agora.
            """
            estados_br = [
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
                'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ]

            # 1. Recupera Código CBO
            cbo_codigo = self.nome_para_cbo.get(dados_solicitacao.cargo.value)

            # 2. CONTAGEM REAL (Baseada no Parquet)
            # Nota: A contagem mostra "quantas pessoas existem com esse cargo nesse ano".
            # Não filtramos a contagem por idade/raça específica para não zerar o mapa (amostra muito pequena),
            # mas mantemos a contagem total/masc/fem para dar contexto.
            stats_por_uf = {}
            
            if cbo_codigo and not self.df_rais.empty:
                filtro = (self.df_rais['cbo_2002'] == str(cbo_codigo)) & (self.df_rais['ano'] == dados_solicitacao.ano)
                df_filtrado = self.df_rais[filtro]

                if not df_filtrado.empty:
                    grupo = df_filtrado.groupby(['sigla_uf', 'sexo']).size().unstack(fill_value=0)
                    for uf in estados_br:
                        if uf in grupo.index:
                            masc = int(grupo.loc[uf].get(1, 0))
                            fem = int(grupo.loc[uf].get(2, 0))
                            stats_por_uf[uf] = {
                                'total': masc + fem,
                                'masculino': masc,
                                'feminino': fem
                            }

            # 3. PREPARAÇÃO DA PREDIÇÃO
            # Agora usamos os dados que vieram do request
            
            # A. Converter Enums (Texto) -> Códigos RAIS (Int) usando seus mappings
            cod_tamanho = mapa_tamanho.get(dados_solicitacao.tamanho_empresa.value, 6)
            cod_escolaridade = mapa_escolaridade.get(dados_solicitacao.escolaridade.value, 9)
            cod_sexo_rais = mapa_sexo.get(dados_solicitacao.sexo.value, 1)
            cod_raca_rais = mapa_raca.get(dados_solicitacao.raca.value, 2)
            
            # B. Target Encoding (Códigos -> Médias do Modelo)
            val_cbo = self.mapa_medias['cbo'].get(str(cbo_codigo), self.media_global)
            val_esc = self.mapa_medias['esc'].get(str(cod_escolaridade), self.media_global)
            val_tam = self.mapa_medias['tam'].get(str(cod_tamanho), self.media_global)
            
            # Setor fixo em TI/Financeiro (17) para comparar maçãs com maçãs, 
            # ou adicione no schema se quiser dinâmico.
            val_setor = self.mapa_medias['setor'].get("17", self.media_global)

            # C. Label Encoding (Sexo e Raça)
            try:
                val_sexo_encoded = self.encoders['sexo'].transform([str(cod_sexo_rais)])[0]
                val_raca_encoded = self.encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
            except:
                val_sexo_encoded, val_raca_encoded = 0, 0

            # 4. CRIAÇÃO DO BATCH (27 Estados)
            input_batch = []
            for uf in estados_br:
                val_uf = self.mapa_medias['uf'].get(uf, self.media_global)
                
                input_batch.append({
                    'cbo_valor': val_cbo,
                    'idade': dados_solicitacao.idade, # <--- Idade dinâmica agora!
                    'esc_valor': val_esc,             # <--- Escolaridade dinâmica!
                    'uf_valor': val_uf,
                    'tam_valor': val_tam,             # <--- Tamanho dinâmico!
                    'setor_valor': val_setor,
                    'sexo': val_sexo_encoded,         # <--- Sexo dinâmico!
                    'raca_cor_valor': val_raca_encoded, # <--- Raça dinâmica!
                    'ano': dados_solicitacao.ano      # <--- Ano dinâmico!
                })

            # 5. EXECUTA MODELO
            df_batch = pd.DataFrame(input_batch)
            try:
                log_salarios = self.modelo.predict(df_batch)
                salarios_reais = np.expm1(log_salarios)
            except Exception as e:
                print(f"Erro predict: {e}")
                salarios_reais = [0] * 27

            # 6. MONTA RESPOSTA
            resultado = []
            for i, uf in enumerate(estados_br):
                stats = stats_por_uf.get(uf, {'total': 0, 'masculino': 0, 'feminino': 0})
                
                resultado.append({
                    "uf": f"br-{uf.lower()}",
                    "salario_estimado": round(float(salarios_reais[i]), 2),
                    # Devolvemos as estatísticas demográficas junto
                    "quantidade_total": stats['total'],
                    "quantidade_masculino": stats['masculino'],
                    "quantidade_feminino": stats['feminino']
                })
                
            return resultado

# Instância global
salario_service = SalarioService()