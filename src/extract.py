"""
Módulo de Extração de Dados
"""
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


class Extract:
    """Classe para extrair dados da camada Silver."""

    def __init__(self):
        self.neon_url = os.getenv('NEON_URL')
        if not self.neon_url:
            raise ValueError("NEON_URL não encontrada no .env")
        self.engine = create_engine(self.neon_url)

    def ler_silver(self):
        """Lê dados da tabela silver_vacinados."""
        query = "SELECT * FROM silver_vacinados"
        df = pd.read_sql(query, self.engine)
        return df
