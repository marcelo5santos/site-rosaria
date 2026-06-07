# Configuração do banco de dados
# Defina aqui a configuração de conexão com o banco de dados
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "rosaria.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operadora TEXT NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                faixa_etaria TEXT NOT NULL,
                valor TEXT NOT NULL,
                imagem TEXT,
                ativo INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.commit()