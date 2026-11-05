"""
Módulo de Carga de Dados
"""
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


class Load:
    """Classe para carregar dados na camada Gold."""

    def __init__(self):
        self.neon_url = os.getenv('NEON_URL')
        if not self.neon_url:
            raise ValueError("NEON_URL não encontrada no .env")
        self.engine = create_engine(self.neon_url)

    def criar_tabela_gold(self):
        """Cria tabela gold_previsoes se não existir."""
        query = """
        CREATE TABLE IF NOT EXISTS gold_previsoes (
            id SERIAL PRIMARY KEY,
            idade INTEGER,
            sexo VARCHAR(50),
            raca_cor VARCHAR(100),
            distrito_sanitario VARCHAR(100),
            dose INTEGER,
            grupo VARCHAR(200),
            data_vacinacao DATE,
            vacina_prevista VARCHAR(200),
            confianca FLOAT,
            data_previsao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
        print("✓ Tabela gold_previsoes criada/verificada")

    def gravar_previsoes(self, df_previsoes):
        """
        Grava previsões na tabela gold_previsoes em modo append.

        Args:
            df_previsoes: DataFrame com colunas:
                - idade, sexo, raca_cor, distrito_sanitario, dose, grupo, data_vacinacao
                - vacina_prevista, confianca
        """
        # Adicionar data_previsao
        df_previsoes['data_previsao'] = datetime.now()

        # Gravar em modo append
        df_previsoes.to_sql(
            'gold_previsoes',
            self.engine,
            if_exists='append',
            index=False
        )

        print(f"✓ {len(df_previsoes)} previsões gravadas na gold_previsoes")
