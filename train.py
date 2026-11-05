"""
Script de Treinamento - Modelo Final (Experimento 5)

Treina o modelo vencedor da Aula 10 e salva para uso futuro.
Configuração: max_depth=12, dias_desde_inicio, grupo
Acurácia esperada: ~81.5%
"""
from src.extract import Extract
from src.ml_model import Classificador

print("=" * 80)
print("TREINAMENTO DO MODELO FINAL - AULA 10")
print("=" * 80)

# Inicializar
print("\n[1/5] Lendo dados da Silver...")
extract = Extract()
df_silver = extract.ler_silver()
print(f"✓ {len(df_silver):,} registros carregados")

# Preparar dados
print("\n[2/5] Preparando dados...")
classificador = Classificador(max_depth=12)  # Experimento 5
X, y = classificador.preparar(df_silver)
print(f"✓ {len(X):,} registros preparados")
print(f"✓ {X.shape[1]} features criadas")
print(f"✓ {len(y.unique())} classes (vacinas)")

# Dividir treino/teste
print("\n[3/5] Dividindo treino/teste...")
X_treino, X_teste, y_treino, y_teste = classificador.dividir(X, y)
print(f"✓ Treino: {len(X_treino):,} | Teste: {len(X_teste):,}")

# Treinar
print("\n[4/5] Treinando modelo...")
classificador.treinar(X_treino, y_treino)

# Avaliar
print("\n[5/5] Avaliando modelo no teste...")
acuracia = classificador.avaliar(X_teste, y_teste)

# Salvar modelo
print("\nSalvando modelo...")
classificador.salvar()

print("\n" + "=" * 80)
print("TREINAMENTO CONCLUÍDO!")
print("=" * 80)
print(f"\n✓ Acurácia final: {acuracia:.2%}")
print(f"✓ Modelo salvo em: modelos/modelo_final.joblib")
print(f"\nPróximo passo:")
print(f"  python prever.py")
