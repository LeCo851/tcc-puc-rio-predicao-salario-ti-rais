import os
import joblib
import pandas as pd
import numpy as np
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
        self.df_rais = None
        
        # O MAPA DE FALLBACK AGORA É CALCULADO NO STARTUP
        self.mapa_fallback = {} 

        # Sequência de Inicialização
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
            
            # Inverte o mapa CBO para busca por nome
            self.nome_para_cbo = {str(v).strip(): str(k) for k, v in self.cbo_map.items()}
            print("[OK] Modelo ML carregado com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Falha crítica ao carregar modelo: {e}")

    def _carregar_dados_rais(self):
        """Carrega a base Parquet para estatísticas e calcula quartis globais."""
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_parquet = os.path.join(diretorio_base, 'dados_rais_lite.parquet')
        
        # Colunas estritamente necessárias (Economia de Memória)
        cols = ['cbo_2002', 'sigla_uf', 'ano', 'sexo', 'idade']
        
        try:
            if os.path.exists(caminho_parquet):
                print(f"[INIT] Carregando Parquet: {caminho_parquet}...")
                self.df_rais = pd.read_parquet(caminho_parquet, columns=cols)
                
                # Otimização de tipos
                self.df_rais['cbo_2002'] = self.df_rais['cbo_2002'].astype('category')
                self.df_rais['sigla_uf'] = self.df_rais['sigla_uf'].astype('category')
                self.df_rais['ano'] = self.df_rais['ano'].astype('int16')
                self.df_rais['sexo'] = self.df_rais['sexo'].astype('int8')
                self.df_rais['idade'] = self.df_rais['idade'].astype('int8')
                
                print(f"[OK] Base RAIS carregada: {len(self.df_rais)} registros.")
                
                # --- CALCULA O FALLBACK DINAMICAMENTE ---
                self._calcular_quartis_globais()
                
            else:
                print("[WARN] Arquivo Parquet não encontrado. Estatísticas dinâmicas desativadas.")
                self.df_rais = pd.DataFrame(columns=cols)
                # Fallback de emergência (Hardcoded)
                self.mapa_fallback = {"JUNIOR": 25, "PLENO": 30, "SENIOR": 38, "ESPECIALISTA": 45}

        except Exception as e:
            print(f"[ERROR] Erro ao ler Parquet: {e}")
            self.df_rais = pd.DataFrame(columns=cols)

    def _calcular_quartis_globais(self):
        """
        Calcula os quartis da base INTEIRA assim que o sistema sobe.
        Serve como 'Plano B' se um cargo específico tiver poucos dados.
        """
        try:
            if not self.df_rais.empty:
                # Filtra idades válidas (18 a 80)
                df_valido = self.df_rais[(self.df_rais['idade'] >= 18) & (self.df_rais['idade'] <= 80)]
                
                stats = df_valido['idade'].describe(percentiles=[0.25, 0.50, 0.75, 0.90])
                
                self.mapa_fallback = {
                    "JUNIOR": int(stats['25%']),
                    "PLENO": int(stats['50%']),
                    "SENIOR": int(stats['75%']),
                    "ESPECIALISTA": int(stats['90%'])
                }
                print(f"[STATS] Quartis Globais Calculados (Fallback): {self.mapa_fallback}")
            else:
                raise ValueError("DataFrame vazio")
        except Exception as e:
            print(f"[WARN] Erro ao calcular stats globais: {e}. Usando valores padrão.")
            self.mapa_fallback = {"JUNIOR": 27, "PLENO": 32, "SENIOR": 40, "ESPECIALISTA": 47}

    def _resolver_idade(self, cargo_nome, ano, idade_manual, faixa_experiencia):
        """
        Lógica Inteligente de Idade:
        1. Se tem Faixa -> Tenta calcular estatística ESPECÍFICA (Cargo + Ano).
           Se não tiver amostra suficiente (>100), usa a GLOBAL (self.mapa_fallback).
        2. Se não tem Faixa -> Usa Idade Manual ou Padrão (32).
        """
        # Se não tem faixa, usa a idade manual ou a mediana global (Plano C)
        if faixa_experiencia is None:
            return idade_manual if idade_manual is not None else self.mapa_fallback.get("PLENO", 32)

        # Tenta calcular estatística ESPECÍFICA DO CARGO
        cbo_codigo = self.nome_para_cbo.get(cargo_nome)
        idade_final = None

        if cbo_codigo and not self.df_rais.empty:
            cbo_limpo = str(cbo_codigo).replace('-', '').strip()
            
            # Filtro por Cargo e Ano
            filtro = (self.df_rais['cbo_2002'].astype(str).str.replace('-', '') == cbo_limpo) & \
                     (self.df_rais['ano'] == ano)
            
            df_filtrado = self.df_rais[filtro]
            
            # Se tiver amostra relevante (> 100 registros), confiamos na estatística específica
            if len(df_filtrado) >= 100:
                stats = df_filtrado['idade'].describe(percentiles=[0.25, 0.50, 0.75, 0.90])
                match faixa_experiencia:
                    case "JUNIOR": idade_final = int(stats['25%'])
                    case "PLENO": idade_final = int(stats['50%'])
                    case "SENIOR": idade_final = int(stats['75%'])
                    case "ESPECIALISTA": idade_final = int(stats['90%'])
                
                # Debug para verificar se funcionou
                print(f"[INFO] Usando idade dinâmica para {cargo_nome}: {idade_final} anos ({faixa_experiencia})")
                return idade_final

        # Se não tiver dados específicos suficientes, usa o GLOBAL CALCULADO NO INÍCIO
        return self.mapa_fallback.get(faixa_experiencia, 32)

    def prever(self, dados):
        """Endpoint Individual (/predict)"""
        # 1. Resolve a idade usando a lógica centralizada
        idade_calculada = self._resolver_idade(
            dados.cargo.value, dados.ano, dados.idade, dados.faixa_experiencia
        )

        cbo_codigo = self.nome_para_cbo.get(dados.cargo.value, "000000")
        cod_tamanho = mapa_tamanho.get(dados.tamanho_empresa.value, 6)
        cod_escolaridade = mapa_escolaridade.get(dados.escolaridade.value, 9)
        cod_setor = mapa_setor.get(dados.setor.value, 18)  # Default para "Instituições Financeiras (Bancos)"
        cod_sexo_rais = 1 if dados.sexo.value == "Masculino" else 2 
        cod_raca_rais = mapa_raca.get(dados.raca.value, 9)

        # Busca médias (Target Encoding)
        val_cbo = self.mapa_medias['cbo'].get(str(cbo_codigo), self.media_global)
        val_esc = self.mapa_medias['esc'].get(str(cod_escolaridade), self.media_global)
        val_uf = self.mapa_medias['uf'].get(dados.uf.upper(), self.media_global)
        val_tam = self.mapa_medias['tam'].get(str(cod_tamanho), self.media_global)
        val_setor = self.mapa_medias['setor'].get(str(cod_setor), self.media_global)

        # Encoders
        try:
            val_sexo_encoded = self.encoders['sexo'].transform([str(cod_sexo_rais)])[0]
            val_raca_encoded = self.encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
        except:
            val_sexo_encoded, val_raca_encoded = 0, 0

        df_input = pd.DataFrame({
            'cbo_valor': [val_cbo],
            'idade': [idade_calculada], # <--- USA A IDADE CALCULADA
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
        """Endpoint Batch para o Mapa (/analise/mapa)"""
        estados_br = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
            'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]

        cbo_codigo = self.nome_para_cbo.get(dados_solicitacao.cargo.value)

        # 1. Resolve a idade usando a lógica centralizada (Dinâmica)
        idade_calculada = self._resolver_idade(
            dados_solicitacao.cargo.value,
            dados_solicitacao.ano,
            dados_solicitacao.idade,
            dados_solicitacao.faixa_experiencia
        )

        # 2. Estatísticas de Contagem (Demografia Real)
        stats_por_uf = {}
        if cbo_codigo and not self.df_rais.empty:
            cbo_limpo = str(cbo_codigo).replace('-', '').strip()
            
            # --- CORREÇÃO AQUI: FILTRO DE ANO ---
            # Antes estava filtrando apenas pelo cargo, agora filtra pelo ANO também
            filtro = (self.df_rais['cbo_2002'].astype(str).str.replace('-', '') == cbo_limpo) & \
                     (self.df_rais['ano'] == dados_solicitacao.ano) # <--- GARANTE QUE O ANO SEJA RESPEITADO

            df_filtrado_stats = self.df_rais[filtro]

            if not df_filtrado_stats.empty:
                grupo = df_filtrado_stats.groupby(['sigla_uf', 'sexo']).size().unstack(fill_value=0)
                for uf in estados_br:
                    if uf in grupo.index:
                        masc = int(grupo.loc[uf].get(1, 0))
                        fem = int(grupo.loc[uf].get(2, 0))
                        stats_por_uf[uf] = {'total': masc+fem, 'masculino': masc, 'feminino': fem}

        # 3. Preparação para Predição em Lote
        cod_tamanho = mapa_tamanho.get(dados_solicitacao.tamanho_empresa.value, 6)
        cod_escolaridade = mapa_escolaridade.get(dados_solicitacao.escolaridade.value, 9)
        cod_setor = mapa_setor.get(dados_solicitacao.setor.value, 17) # <--- CORREÇÃO AQUI
        cod_sexo_rais = 1 # Padrão Masculino para o mapa (ou parametrizar)
        cod_raca_rais = 2

        val_cbo = self.mapa_medias['cbo'].get(str(cbo_codigo), self.media_global)
        val_esc = self.mapa_medias['esc'].get(str(cod_escolaridade), self.media_global)
        val_tam = self.mapa_medias['tam'].get(str(cod_tamanho), self.media_global)
        val_setor = self.mapa_medias['setor'].get(str(cod_setor), self.media_global) # <--- E AQUI

        try:
            val_sexo_encoded = self.encoders['sexo'].transform([str(cod_sexo_rais)])[0]
            val_raca_encoded = self.encoders['raca_cor_valor'].transform([str(cod_raca_rais)])[0]
        except:
            val_sexo_encoded, val_raca_encoded = 0, 0

        # 4. Cria Batch (27 linhas, uma para cada UF)
        input_batch = []
        for uf in estados_br:
            val_uf = self.mapa_medias['uf'].get(uf, self.media_global)
            input_batch.append({
                'cbo_valor': val_cbo,
                'idade': idade_calculada, # <--- USA A IDADE CALCULADA DINAMICAMENTE
                'esc_valor': val_esc,
                'uf_valor': val_uf,
                'tam_valor': val_tam,
                'setor_valor': val_setor,
                'sexo': val_sexo_encoded,
                'raca_cor_valor': val_raca_encoded,
                'ano': dados_solicitacao.ano
            })

        # 5. Predição Otimizada
        df_batch = pd.DataFrame(input_batch)
        try:
            log_salarios = self.modelo.predict(df_batch)
            salarios_reais = np.expm1(log_salarios)
        except Exception as e:
            print(f"Erro predict batch: {e}")
            salarios_reais = [0] * 27

        # 6. Montagem da Resposta
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

# Instância Singleton
salario_service = SalarioService()