import os
from telegram.ext import ApplicationBuilder
from config import TOKEN
from commands import registrar_handlers
from server import start_server

if os.getenv("RUN_SERVER") == "1":
    start_server()

app = ApplicationBuilder().token(TOKEN).build()
registrar_handlers(app)
app.run_polling()
