import psycopg2
import os
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    result = urlparse(database_url)
    return psycopg2.connect(
        host=result.hostname,
        database=result.path[1:],
        user=result.username,
        password=result.password,
        port=result.port or 5432,
        sslmode='require'
    )

def add_usuario(telegram_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (telegram_id, nome) VALUES (%s, %s) ON CONFLICT (telegram_id) DO NOTHING",
        (telegram_id, nome)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_usuario(telegram_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios WHERE telegram_id = %s", (telegram_id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario

def add_cartao(usuario_id, nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cartoes (usuario_id, nome) VALUES (%s, %s) RETURNING id",
        (usuario_id, nome)
    )
    cartao_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return cartao_id

def get_cartoes(usuario_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM cartoes WHERE usuario_id = %s", (usuario_id,))
    cartoes = cur.fetchall()
    cur.close()
    conn.close()
    return cartoes

def get_categorias():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM categorias ORDER BY nome")
    categorias = cur.fetchall()
    cur.close()
    conn.close()
    return categorias

def add_gasto(usuario_id, tipo_pagamento, cartao_id, categoria_id, valor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gastos (usuario_id, tipo_pagamento, cartao_id, categoria_id, valor) VALUES (%s, %s, %s, %s, %s)",
        (usuario_id, tipo_pagamento, cartao_id, categoria_id, valor)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_gastos(usuario_id, mes=None, ano=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM gastos WHERE usuario_id = %s"
    params = [usuario_id]
    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_gasto) = %s AND EXTRACT(YEAR FROM data_gasto) = %s"
        params.extend([mes, ano])
    query += " ORDER BY data_gasto DESC"
    cur.execute(query, params)
    gastos = cur.fetchall()
    cur.close()
    conn.close()
    return gastos

def get_resumo(usuario_id, mes=None, ano=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT categoria_id, tipo_pagamento, SUM(valor) as total FROM gastos WHERE usuario_id = %s"
    params = [usuario_id]
    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data_gasto) = %s AND EXTRACT(YEAR FROM data_gasto) = %s"
        params.extend([mes, ano])
    query += " GROUP BY categoria_id, tipo_pagamento ORDER BY categoria_id"
    cur.execute(query, params)
    resumo = cur.fetchall()
    cur.close()
    conn.close()
    return resumo

def get_gastos_para_pdf(usuario_id, mes, ano):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT 
            g.data_gasto, 
            c.nome AS categoria, 
            g.tipo_pagamento, 
            COALESCE(ca.nome, 'Dinheiro') AS cartao, 
            g.valor
        FROM gastos g
        LEFT JOIN categorias c ON g.categoria_id = c.id
        LEFT JOIN cartoes ca ON g.cartao_id = ca.id
        WHERE g.usuario_id = %s
          AND EXTRACT(MONTH FROM g.data_gasto) = %s
          AND EXTRACT(YEAR FROM g.data_gasto) = %s
        ORDER BY g.data_gasto ASC
        """,
        (usuario_id, mes, ano)
    )
    gastos = cur.fetchall()
    cur.close()
    conn.close()
    return gastos if gastos else []

