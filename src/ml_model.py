"""
Módulo de Machine Learning - Classificador de Vacinas
Modelo Final: Experimento 5 (max_depth=12, dias_desde_inicio, grupo)
"""
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.dummy import DummyClassifier
import joblib
import os


class Classificador:
    """Classificador de vacinas usando Decision Tree."""

    ALVO = "vacina"
    RANDOM_STATE = 42

    def __init__(self, max_depth=12, min_registros=50):
        """
        Inicializa o classificador com os hiperparâmetros do modelo final.

        Args:
            max_depth: Profundidade máxima da árvore (Experimento 5: 12)
            min_registros: Mínimo de registros por classe
        """
        self.max_depth = max_depth
        self.min_registros = min_registros
        self.modelo = DecisionTreeClassifier(
            max_depth=max_depth,
            random_state=self.RANDOM_STATE
        )
        self.colunas_treino = None
        self.data_minima = None  # Para calcular dias_desde_inicio

    def preparar(self, df):
        """
        Prepara dados para treino (mesma lógica do Experimento 5).

        Features:
        - dias_desde_inicio (temporal contínua)
        - idade, dose (numéricas)
        - sexo, raca_cor, distrito_sanitario, grupo (categóricas)

        Args:
            df: DataFrame da Silver

        Returns:
            X, y: Features e target
        """
        df = df.copy()

        # Converter data
        df['data_vacinacao'] = pd.to_datetime(df['data_vacinacao'])

        # Feature temporal: dias desde o início
        self.data_minima = df['data_vacinacao'].min()
        df['dias_desde_inicio'] = (df['data_vacinacao'] - self.data_minima).dt.days

        # Features numéricas
        features_numericas = ['idade', 'dose', 'dias_desde_inicio']

        # Features categóricas
        features_categoricas = ['sexo', 'raca_cor', 'distrito_sanitario']

        # Adicionar grupo se disponível
        if 'grupo' in df.columns:
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

        # Guardar colunas para uso futuro
        self.colunas_treino = X.columns.tolist()

        return X, y

    def preparar_entrada(self, df_novos):
        """
        Prepara novos dados para previsão (MESMA LÓGICA do preparar).

        IMPORTANTE: Reproduz exatamente a engenharia de features do treino.

        Args:
            df_novos: DataFrame com perfis novos (mesmo schema da silver)

        Returns:
            X: Features preparadas com as mesmas colunas do treino
        """
        df = df_novos.copy()

        # Converter data
        df['data_vacinacao'] = pd.to_datetime(df['data_vacinacao'])

        # Feature temporal: dias desde o início (MESMO data_minima do treino!)
        if self.data_minima is None:
            raise ValueError("Modelo não foi treinado. Execute preparar() primeiro.")

        df['dias_desde_inicio'] = (df['data_vacinacao'] - self.data_minima).dt.days

        # Features numéricas
        features_numericas = ['idade', 'dose', 'dias_desde_inicio']

        # Features categóricas
        features_categoricas = ['sexo', 'raca_cor', 'distrito_sanitario']

        # Adicionar grupo se disponível
        if 'grupo' in df.columns:
            features_categoricas.append('grupo')

        # Preparar X
        colunas = features_numericas + features_categoricas
        X = pd.get_dummies(df[colunas], columns=features_categoricas, dtype=int)

        # GARANTIR que X tenha as mesmas colunas do treino
        # Adicionar colunas faltantes com 0
        for col in self.colunas_treino:
            if col not in X.columns:
                X[col] = 0

        # Remover colunas extras (categorias novas que o modelo nunca viu)
        X = X[self.colunas_treino]

        return X

    def dividir(self, X, y):
        """
        MÉTODO OBRIGATÓRIO - NÃO ALTERAR.

        Divide dados em treino e teste.
        """
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    def treinar(self, X_treino, y_treino):
        """Treina o modelo."""
        self.modelo.fit(X_treino, y_treino)
        print("✓ Modelo treinado")

    def avaliar(self, X_teste, y_teste):
        """Avalia o modelo no conjunto de teste."""
        y_pred = self.modelo.predict(X_teste)
        acuracia = accuracy_score(y_teste, y_pred)
        print(f"\n{'='*60}")
        print(f"ACURÁCIA NO TESTE: {acuracia:.2%}")
        print(f"{'='*60}\n")
        print(classification_report(y_teste, y_pred, zero_division=0))
        return acuracia

    def prever(self, X):
        """
        Faz previsões para novos dados.

        Returns:
            previsoes: Array com as classes previstas
            confiancas: Array com as probabilidades máximas
        """
        previsoes = self.modelo.predict(X)
        probabilidades = self.modelo.predict_proba(X)
        confiancas = probabilidades.max(axis=1)  # Confiança = maior probabilidade

        return previsoes, confiancas

    def salvar(self, caminho='modelos/modelo_final.joblib'):
        """
        Salva o modelo treinado e metadados.

        Args:
            caminho: Caminho para salvar o modelo
        """
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho), exist_ok=True)

        # Salvar modelo e metadados
        dados = {
            'modelo': self.modelo,
            'colunas_treino': self.colunas_treino,
            'data_minima': self.data_minima,
            'max_depth': self.max_depth,
            'min_registros': self.min_registros
        }

        joblib.dump(dados, caminho)
        print(f"✓ Modelo salvo em {caminho}")

    def carregar(self, caminho='modelos/modelo_final.joblib'):
        """
        Carrega modelo treinado e metadados.

        Args:
            caminho: Caminho do modelo salvo
        """
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Modelo não encontrado: {caminho}")

        dados = joblib.load(caminho)

        self.modelo = dados['modelo']
        self.colunas_treino = dados['colunas_treino']
        self.data_minima = dados['data_minima']
        self.max_depth = dados['max_depth']
        self.min_registros = dados['min_registros']

        print(f"✓ Modelo carregado de {caminho}")
        print(f"  - max_depth: {self.max_depth}")
        print(f"  - Features: {len(self.colunas_treino)}")
        print(f"  - Data mínima (referência): {self.data_minima}")
