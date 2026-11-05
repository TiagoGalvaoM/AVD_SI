"""
Script de Previsão - Aula 11

Carrega o modelo salvo, testa sua acurácia e faz previsões para perfis novos.
As previsões são gravadas na tabela gold_previsoes.
"""
import pandas as pd
from src.extract import Extract
from src.load import Load
from src.ml_model import Classificador

print("=" * 80)
print("PREVISÃO DE VACINAS - AULA 11")
print("=" * 80)

# ============================================================================
# 1. CARREGAR MODELO
# ============================================================================
print("\n[1/6] Carregando modelo salvo...")
classificador = Classificador()
classificador.carregar()

# ============================================================================
# 2. VALIDAR MODELO COM TESTE ORIGINAL
# ============================================================================
print("\n[2/6] Validando modelo com dados de teste...")
print("(A acurácia deve ser igual à do train.py)\n")

extract = Extract()
df_silver = extract.ler_silver()

# Preparar dados (SEM retreinar!)
X, y = classificador.preparar(df_silver)
X_treino, X_teste, y_treino, y_teste = classificador.dividir(X, y)

# Avaliar com modelo carregado
acuracia = classificador.avaliar(X_teste, y_teste)
print(f"✓ Validação OK: {acuracia:.2%}")

# ============================================================================
# 3. CRIAR PERFIS NOVOS PARA PREVISÃO
# ============================================================================
print("\n[3/6] Criando perfis novos para previsão...")

perfis_novos = pd.DataFrame([
    {
        # Perfil 1: Criança (5 anos) - deve prever vacina pediátrica
        'idade': 5,
        'sexo': 'FEMININO',
        'raca_cor': 'BRANCA',
        'distrito_sanitario': 'DS 1',
        'dose': 1,
        'grupo': 'CRIANÇAS DE 05 A 11 ANOS',
        'data_vacinacao': '2022-03-15'
    },
    {
        # Perfil 2: Dose de reforço (3ª dose)
        'idade': 45,
        'sexo': 'MASCULINO',
        'raca_cor': 'PARDA',
        'distrito_sanitario': 'DS 3',
        'dose': 3,
        'grupo': 'PÚBLICO EM GERAL (18 A 59 ANOS)',
        'data_vacinacao': '2022-02-10'
    },
    {
        # Perfil 3: Idoso (1ª dose) - grupo prioritário
        'idade': 75,
        'sexo': 'FEMININO',
        'raca_cor': 'PRETA',
        'distrito_sanitario': 'DS 2',
        'dose': 1,
        'grupo': 'IDOSOS ACIMA DE 60 ANOS',
        'data_vacinacao': '2021-06-20'
    },
    {
        # Perfil 4: Distrito INEXISTENTE (categoria nova que modelo nunca viu)
        'idade': 30,
        'sexo': 'MASCULINO',
        'raca_cor': 'AMARELA',
        'distrito_sanitario': 'DS INEXISTENTE',  # CATEGORIA NOVA!
        'dose': 2,
        'grupo': 'PÚBLICO EM GERAL (18 A 59 ANOS)',
        'data_vacinacao': '2021-12-15'
    },
    {
        # Perfil 5: Data FORA DO PERÍODO (futuro)
        'idade': 28,
        'sexo': 'FEMININO',
        'raca_cor': 'INDÍGENA',
        'distrito_sanitario': 'DS 4',
        'dose': 1,
        'grupo': 'PÚBLICO EM GERAL (18 A 59 ANOS)',
        'data_vacinacao': '2025-01-01'  # DATA FUTURA!
    },
    {
        # Perfil 6: Criança com dose de reforço pediátrica
        'idade': 8,
        'sexo': 'MASCULINO',
        'raca_cor': 'BRANCA',
        'distrito_sanitario': 'DS 5',
        'dose': 2,
        'grupo': 'CRIANÇAS DE 05 A 11 ANOS',
        'data_vacinacao': '2022-04-20'
    },
    {
        # Perfil 7: Adulto jovem no início da campanha
        'idade': 22,
        'sexo': 'FEMININO',
        'raca_cor': 'PARDA',
        'distrito_sanitario': 'DS 6',
        'dose': 1,
        'grupo': 'PÚBLICO EM GERAL (18 A 59 ANOS)',
        'data_vacinacao': '2021-05-10'  # DATA MUITO ANTIGA
    }
])

print(f"✓ {len(perfis_novos)} perfis criados:")
print("\n  1. Criança de 5 anos (vacina pediátrica)")
print("  2. Adulto com dose de reforço (3ª dose)")
print("  3. Idoso de 75 anos (grupo prioritário)")
print("  4. Perfil com distrito INEXISTENTE")
print("  5. Perfil com data FUTURA (2025)")
print("  6. Criança com 2ª dose")
print("  7. Adulto jovem no início da campanha (2021)")

# ============================================================================
# 4. PREPARAR NOVOS DADOS
# ============================================================================
print("\n[4/6] Preparando novos dados para previsão...")
X_novos = classificador.preparar_entrada(perfis_novos)
print(f"✓ {len(X_novos)} perfis preparados")
print(f"✓ {X_novos.shape[1]} features (mesmo número do treino)")

# ============================================================================
# 5. FAZER PREVISÕES
# ============================================================================
print("\n[5/6] Fazendo previsões...")
previsoes, confiancas = classificador.prever(X_novos)

# Adicionar previsões ao DataFrame
perfis_novos['vacina_prevista'] = previsoes
perfis_novos['confianca'] = confiancas

print("\n" + "=" * 80)
print("RESULTADOS DAS PREVISÕES")
print("=" * 80)

for i, row in perfis_novos.iterrows():
    print(f"\nPerfil {i+1}:")
    print(f"  Idade: {row['idade']} | Dose: {row['dose']} | Data: {row['data_vacinacao']}")
    print(f"  Distrito: {row['distrito_sanitario']} | Grupo: {row['grupo'][:40]}...")
    print(f"  → PREVISÃO: {row['vacina_prevista']}")
    print(f"  → CONFIANÇA: {row['confianca']:.1%}")

# ============================================================================
# 6. GRAVAR NA GOLD
# ============================================================================
print("\n[6/6] Gravando previsões na Gold...")
load = Load()
load.criar_tabela_gold()
load.gravar_previsoes(perfis_novos)

print("\n" + "=" * 80)
print("PREVISÕES CONCLUÍDAS!")
print("=" * 80)
print(f"\n✓ {len(perfis_novos)} previsões gravadas em gold_previsoes")
print(f"\nPróximo passo:")
print(f"  - Consultar gold_previsoes no SQL Editor do Neon")
print(f"  - Query: SELECT * FROM gold_previsoes ORDER BY data_previsao DESC;")
