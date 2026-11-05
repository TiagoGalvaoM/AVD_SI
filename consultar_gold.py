"""
Script para Consultar a Tabela gold_previsoes
"""
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 80)
print("CONSULTA DA TABELA GOLD_PREVISOES")
print("=" * 80)

# Conectar ao banco
neon_url = os.getenv('NEON_URL')
engine = create_engine(neon_url)

# Consultar previsões
query = """
SELECT
    id,
    idade,
    sexo,
    distrito_sanitario,
    dose,
    grupo,
    data_vacinacao,
    vacina_prevista,
    ROUND(confianca::numeric, 2) as confianca,
    data_previsao
FROM gold_previsoes
ORDER BY data_previsao DESC
"""

df = pd.read_sql(query, engine)

print(f"\n✓ {len(df)} previsões encontradas:\n")

# Configurar pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 40)

print(df.to_string(index=False))

print("\n" + "=" * 80)
print("ANÁLISE DAS PREVISÕES")
print("=" * 80)

print("\nDistribuição de vacinas previstas:")
print(df['vacina_prevista'].value_counts())

print("\nConfiança média por vacina:")
print(df.groupby('vacina_prevista')['confianca'].mean().round(2))

print("\n" + "=" * 80)
