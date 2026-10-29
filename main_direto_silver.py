"""ETL simplificado: API → Silver (sem Bronze)."""
from src.extract import Extract
from src.transform import Transform
from src.load import Load
import pandas as pd

extract = Extract()
transform = Transform()
load = Load()

print("=" * 80)
print("ETL SIMPLIFICADO: API → SILVER")
print("=" * 80)

# API -> Dados brutos
print("\n[1/3] Extraindo dados da API...")
registros = extract.ler_api()
print(f"✓ {len(registros)} registros obtidos da API")

# Converter para DataFrame
print("\n[2/3] Transformando dados...")
df_bronze = pd.DataFrame(registros)
df_silver = transform.limpar(df_bronze)
print(f"✓ {len(df_silver)} registros limpos")

# Salvar na Silver
print("\n[3/3] Salvando na Silver (NeonDB)...")
load.salvar_silver(df_silver)
print("✓ Dados salvos com sucesso!")

print("\n" + "=" * 80)
print("ETL CONCLUÍDO")
print("=" * 80)
print(f"\nTabela 'silver_vacinados' criada com {len(df_silver):,} registros")
print("\nAgora você pode executar o classificador:")
print("  jupyter notebook atividade_aula10_classificador.ipynb")
