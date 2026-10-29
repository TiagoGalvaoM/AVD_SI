"""
Atividade Aula 10 - Classificador de Vacinas
Objetivo: Atingir >80% de acurácia usando apenas DecisionTreeClassifier
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.dummy import DummyClassifier
from src.extract import Extract

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("=" * 80)
print("ATIVIDADE AULA 10 - CLASSIFICADOR DE VACINAS")
print("=" * 80)

# ============================================================================
# 1. LEITURA DOS DADOS
# ============================================================================
print("\n[1/10] Lendo dados da Silver...")
extract = Extract()
df_silver = extract.ler_silver()
print(f"✓ {len(df_silver):,} registros carregados")

# ============================================================================
# 2. ANÁLISE INICIAL
# ============================================================================
print("\n[2/10] Análise inicial...")
print(f"\nColunas disponíveis: {list(df_silver.columns)}")
print(f"\nDistribuição das vacinas:")
print(df_silver['vacina'].value_counts())
vacina_mais_comum = df_silver['vacina'].value_counts().index[0]
prop_mais_comum = (df_silver['vacina'].value_counts().iloc[0] / len(df_silver)) * 100
print(f"\nVacina mais frequente: {vacina_mais_comum} ({prop_mais_comum:.1f}%)")

# ============================================================================
# 3. PREPARAÇÃO DOS DADOS
# ============================================================================
print("\n[3/10] Preparando dados...")

class PreparadorAvancado:
    """Preparador com features melhoradas."""

    ALVO = "vacina"

    def __init__(self, min_registros=50):
        self.min_registros = min_registros

    def preparar(self, df, usar_dias_inicio=True, adicionar_grupo=True):
        df = df.copy()

        # Converter data
        df['data_vacinacao'] = pd.to_datetime(df['data_vacinacao'])

        # Features temporais
        df['ano'] = df['data_vacinacao'].dt.year
        df['mes'] = df['data_vacinacao'].dt.month

        # MELHOR REPRESENTAÇÃO: dias desde o início
        if usar_dias_inicio:
            data_minima = df['data_vacinacao'].min()
            df['dias_desde_inicio'] = (df['data_vacinacao'] - data_minima).dt.days

        # Features numéricas base
        features_numericas = ['idade', 'dose']

        if usar_dias_inicio:
            features_numericas.append('dias_desde_inicio')
        else:
            features_numericas.extend(['ano', 'mes'])

        # Features categóricas
        features_categoricas = ['sexo', 'raca_cor', 'distrito_sanitario']

        # Adicionar grupo se disponível e solicitado
        if adicionar_grupo and 'grupo' in df.columns:
            features_categoricas.append('grupo')

        # Remover nulos
        todas_features = features_numericas + [self.ALVO]
        df = df.dropna(subset=todas_features)

        # Filtrar vacinas com poucos registros
        contagem = df[self.ALVO].value_counts()
        manter = contagem[contagem >= self.min_registros].index
        df = df[df[self.ALVO].isin(manter)]

        # Preparar X e y
        colunas = features_numericas + features_categoricas
        X = pd.get_dummies(df[colunas], columns=features_categoricas, dtype=int)
        y = df[self.ALVO]

        return X, y

    def dividir(self, X, y):
        """MÉTODO OBRIGATÓRIO - NÃO ALTERAR"""
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preparador = PreparadorAvancado()

# ============================================================================
# 4. DIVISÃO TREINO/TESTE
# ============================================================================
print("\n[4/10] Dividindo treino/teste...")

# Configuração com dias_desde_inicio e grupo
X, y = preparador.preparar(df_silver, usar_dias_inicio=True, adicionar_grupo=True)
X_treino, X_teste, y_treino, y_teste = preparador.dividir(X, y)

print(f"Treino: {len(X_treino):,} | Teste: {len(X_teste):,}")
print(f"Features: {X_treino.shape[1]}")

# ============================================================================
# 5. LINHA DE BASE
# ============================================================================
print("\n[5/10] Calculando linha de base...")
dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
dummy.fit(X_treino, y_treino)
acuracia_baseline = accuracy_score(y_teste, dummy.predict(X_teste))
print(f"Linha de base (sempre chutar {vacina_mais_comum[:30]}...): {acuracia_baseline:.1%}")

# ============================================================================
# 6. VALIDAÇÃO CRUZADA
# ============================================================================
print("\n[6/10] Configurando validação cruzada...")

def avaliar_cv(modelo, X_treino, y_treino, cv=5):
    """Avalia modelo com validação cruzada."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(modelo, X_treino, y_treino, cv=skf, scoring='accuracy')
    return scores.mean(), scores.std()

# ============================================================================
# 7. EXPERIMENTOS
# ============================================================================
print("\n[7/10] Executando experimentos...")

resultados = []

# Experimento 0: Baseline (original)
print("\n  Experimento 0: Modelo original (max_depth=4)...")
X_orig, y_orig = preparador.preparar(df_silver, usar_dias_inicio=False, adicionar_grupo=False)
X_tr_orig, X_te_orig, y_tr_orig, y_te_orig = preparador.dividir(X_orig, y_orig)
modelo_0 = DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_0, X_tr_orig, y_tr_orig)
resultados.append({
    'Exp': 0,
    'Descrição': 'Original (ano+mes, max_depth=4)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 1: Dias desde início
print("\n  Experimento 1: Dias desde início...")
modelo_1 = DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_1, X_treino, y_treino)
resultados.append({
    'Exp': 1,
    'Descrição': 'Dias desde início + grupo (max_depth=4)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 2: max_depth=6
print("\n  Experimento 2: Aumentar profundidade para 6...")
modelo_2 = DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_2, X_treino, y_treino)
resultados.append({
    'Exp': 2,
    'Descrição': 'Dias desde início + grupo (max_depth=6)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 3: max_depth=8
print("\n  Experimento 3: Aumentar profundidade para 8...")
modelo_3 = DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_3, X_treino, y_treino)
resultados.append({
    'Exp': 3,
    'Descrição': 'Dias desde início + grupo (max_depth=8)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 4: max_depth=10
print("\n  Experimento 4: Aumentar profundidade para 10...")
modelo_4 = DecisionTreeClassifier(max_depth=10, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_4, X_treino, y_treino)
resultados.append({
    'Exp': 4,
    'Descrição': 'Dias desde início + grupo (max_depth=10)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 5: max_depth=12
print("\n  Experimento 5: Aumentar profundidade para 12...")
modelo_5 = DecisionTreeClassifier(max_depth=12, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_5, X_treino, y_treino)
resultados.append({
    'Exp': 5,
    'Descrição': 'Dias desde início + grupo (max_depth=12)',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# Experimento 6: max_depth=10 + min_samples_leaf=5
print("\n  Experimento 6: max_depth=10 + min_samples_leaf=5...")
modelo_6 = DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, random_state=RANDOM_STATE)
cv_mean, cv_std = avaliar_cv(modelo_6, X_treino, y_treino)
resultados.append({
    'Exp': 6,
    'Descrição': 'max_depth=10 + min_samples_leaf=5',
    'CV_média': cv_mean,
    'CV_std': cv_std
})
print(f"    CV: {cv_mean:.1%} ± {cv_std:.1%}")

# ============================================================================
# 8. ESCOLHA DO MELHOR MODELO
# ============================================================================
print("\n[8/10] Escolhendo melhor modelo...")

df_resultados = pd.DataFrame(resultados).sort_values('CV_média', ascending=False)
print("\n" + "=" * 80)
print("TABELA DE EXPERIMENTOS")
print("=" * 80)
print(df_resultados.to_string(index=False))

df_resultados.to_csv('resultados_experimentos.csv', index=False)
print("\n✓ Salvo em 'resultados_experimentos.csv'")

melhor = df_resultados.iloc[0]
print(f"\n🏆 MELHOR CONFIGURAÇÃO:")
print(f"   Experimento {int(melhor['Exp'])}: {melhor['Descrição']}")
print(f"   CV: {melhor['CV_média']:.2%} ± {melhor['CV_std']:.2%}")

# ============================================================================
# 9. TREINAR MODELO FINAL
# ============================================================================
print("\n[9/10] Treinando modelo final...")

# Recriar modelo com melhor configuração
if int(melhor['Exp']) == 0:
    modelo_final = DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE)
    modelo_final.fit(X_tr_orig, y_tr_orig)
    y_pred = modelo_final.predict(X_te_orig)
    acuracia_final = accuracy_score(y_te_orig, y_pred)
else:
    # Usar modelo com dias_desde_inicio e grupo
    if int(melhor['Exp']) == 1:
        modelo_final = DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE)
    elif int(melhor['Exp']) == 2:
        modelo_final = DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE)
    elif int(melhor['Exp']) == 3:
        modelo_final = DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE)
    elif int(melhor['Exp']) == 4:
        modelo_final = DecisionTreeClassifier(max_depth=10, random_state=RANDOM_STATE)
    elif int(melhor['Exp']) == 5:
        modelo_final = DecisionTreeClassifier(max_depth=12, random_state=RANDOM_STATE)
    elif int(melhor['Exp']) == 6:
        modelo_final = DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, random_state=RANDOM_STATE)

    modelo_final.fit(X_treino, y_treino)
    y_pred = modelo_final.predict(X_teste)
    acuracia_final = accuracy_score(y_teste, y_pred)

# ============================================================================
# 10. AVALIAÇÃO FINAL
# ============================================================================
print("\n[10/10] Avaliação final no teste...")

print("\n" + "=" * 80)
print("RESULTADO FINAL")
print("=" * 80)
print(f"\n🎯 ACURÁCIA FINAL NO TESTE: {acuracia_final:.2%}")

if acuracia_final > 0.8:
    print(f"\n✅ META ATINGIDA! Superou 80% com margem de +{(acuracia_final - 0.8)*100:.2f} pontos percentuais!")
else:
    print(f"\n⚠️  Meta não atingida. Faltaram {(0.8 - acuracia_final)*100:.2f} pontos percentuais.")
    print(f"   Mas melhorou {(acuracia_final - acuracia_baseline)*100:.1f} pontos em relação à linha de base!")

print("\n" + "=" * 80)
print("CLASSIFICATION REPORT")
print("=" * 80)
if int(melhor['Exp']) == 0:
    print(classification_report(y_te_orig, y_pred, zero_division=0))
else:
    print(classification_report(y_teste, y_pred, zero_division=0))

# Matriz de confusão
print("\nGerando matriz de confusão...")
fig, ax = plt.subplots(figsize=(12, 10))
if int(melhor['Exp']) == 0:
    ConfusionMatrixDisplay.from_predictions(y_te_orig, y_pred, ax=ax, cmap='Oranges', xticks_rotation=45)
else:
    ConfusionMatrixDisplay.from_predictions(y_teste, y_pred, ax=ax, cmap='Oranges', xticks_rotation=45)
ax.set_title('Matriz de Confusão - Modelo Final', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('matriz_confusao_final.png', dpi=150, bbox_inches='tight')
print("✓ Salvo em 'matriz_confusao_final.png'")

# Feature importances
print("\nTop 10 features mais importantes:")
if int(melhor['Exp']) == 0:
    importancias = pd.Series(modelo_final.feature_importances_, index=X_tr_orig.columns)
else:
    importancias = pd.Series(modelo_final.feature_importances_, index=X_treino.columns)
print(importancias.sort_values(ascending=False).head(10))

print("\n" + "=" * 80)
print("ATIVIDADE CONCLUÍDA!")
print("=" * 80)
print(f"\nArquivos gerados:")
print(f"  ✓ resultados_experimentos.csv")
print(f"  ✓ matriz_confusao_final.png")
print(f"\nPróximo passo:")
print(f"  - Abrir o Jupyter Notebook para análise completa e apresentação")
print(f"  - jupyter notebook atividade_aula10_classificador.ipynb")
