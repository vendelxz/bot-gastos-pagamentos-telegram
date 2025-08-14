import os
from telegram.ext import ApplicationBuilder
from config import TOKEN
from commands import registrar_handlers
from server import start_server
from database import get_connection

if os.getenv("RUN_SERVER") == "1":
    start_server()

try:
    conn = get_connection()
    conn.close()
    print("✅ Conexão com banco Supabase estabelecida com sucesso.")
except Exception as e:
    print(f"❌ Erro ao conectar no banco: {e}")

app = ApplicationBuilder().token(TOKEN).build()
registrar_handlers(app)
app.run_polling()
