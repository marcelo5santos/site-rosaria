from database import get_connection


def listar_planos_ativos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT *
            FROM planos
            WHERE ativo = 1
            ORDER BY id DESC
        """).fetchall()


def listar_planos_admin():
    with get_connection() as conn:
        return conn.execute("""
            SELECT *
            FROM planos
            ORDER BY id DESC
        """).fetchall()


def criar_plano(operadora, titulo, descricao, faixa_etaria, valor, imagem=None):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO planos (
                operadora,
                titulo,
                descricao,
                faixa_etaria,
                valor,
                imagem,
                ativo
            )
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (operadora, titulo, descricao, faixa_etaria, valor, imagem))

        conn.commit()


def desativar_plano_por_id(plano_id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE planos
            SET ativo = 0
            WHERE id = ?
        """, (plano_id,))

        conn.commit()
