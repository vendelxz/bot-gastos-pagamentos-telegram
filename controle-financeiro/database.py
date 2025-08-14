import psycopg2
import os
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
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
    cur.execute("INSERT INTO cartoes (usuario_id, nome) VALUES (%s, %s)", (usuario_id, nome))
    conn.commit()
    cur.close()
    conn.close()

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

def add_gasto(usuario_id, tipo_pagamento, cartao_id, categoria, valor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO gastos (usuario_id, tipo_pagamento, cartao_id, categoria, valor) VALUES (%s, %s, %s, %s, %s)",
        (usuario_id, tipo_pagamento, cartao_id, categoria, valor)
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
        query += " AND EXTRACT(MONTH FROM data) = %s AND EXTRACT(YEAR FROM data) = %s"
        params.extend([mes, ano])
    query += " ORDER BY data DESC"
    cur.execute(query, params)
    gastos = cur.fetchall()
    cur.close()
    conn.close()
    return gastos

def get_resumo(usuario_id, mes=None, ano=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT categoria, tipo_pagamento, SUM(valor) as total FROM gastos WHERE usuario_id = %s"
    params = [usuario_id]
    if mes and ano:
        query += " AND EXTRACT(MONTH FROM data) = %s AND EXTRACT(YEAR FROM data) = %s"
        params.extend([mes, ano])
    query += " GROUP BY categoria, tipo_pagamento ORDER BY categoria"
    cur.execute(query, params)
    resumo = cur.fetchall()
    cur.close()
    conn.close()
    return resumo
