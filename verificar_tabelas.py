"""Script para verificar tabelas existentes no NeonDB antes de executar o ETL."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

NEON_URL = os.getenv("NEON_URL")

print("=" * 80)
print("VERIFICANDO TABELAS EXISTENTES NO NEONDB")
print("=" * 80)

try:
    engine = create_engine(NEON_URL)
    inspector = inspect(engine)

    # Listar todas as tabelas
    tables = inspector.get_table_names()

    print(f"\nTotal de tabelas encontradas: {len(tables)}")
    print("\nTabelas existentes:")
    for i, table in enumerate(tables, 1):
        print(f"  {i}. {table}")

    # Verificar se a tabela do projeto já existe
    projeto_tabela = "silver_vacinados"
    if projeto_tabela in tables:
        print(f"\n⚠️  ATENÇÃO: A tabela '{projeto_tabela}' JÁ EXISTE")
        print("    Ela será SUBSTITUÍDA ao executar o ETL (if_exists='replace')")
    else:
        print(f"\n✓ A tabela '{projeto_tabela}' ainda não existe")
        print("   Será criada ao executar o ETL")

    # Identificar tabelas do NexoClima (não devem ser tocadas)
    tabelas_nexoclima = [t for t in tables if 'nexo' in t.lower() or 'clima' in t.lower()]
    if tabelas_nexoclima:
        print(f"\n🔒 Tabelas do NexoClima identificadas (NÃO serão alteradas):")
        for tabela in tabelas_nexoclima:
            print(f"   - {tabela}")

    engine.dispose()
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO CONCLUÍDA")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ Erro ao conectar no NeonDB: {e}")
    print("\nVerifique se a NEON_URL está correta no arquivo .env")
