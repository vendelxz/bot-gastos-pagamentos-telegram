
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN
from server import start_server
import os 

# Funções de comando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou o Controlador de gastos 💰\n"
        "Comandos disponíveis:\n"
        "/gasto - registrar gasto\n"
        "/resumo - ver resumo do mês\n"
        "/pdf - gerar PDF com gastos"
    )

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Funcionalidade de registrar gasto ainda será implementada.")

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Funcionalidade de resumo ainda será implementada.")

async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Funcionalidade de gerar PDF ainda será implementada.")

# Inicia servidor HTTP em background caso queira
if os.getenv("RUN_SERVER") == "1":
    start_server()

# Bot Telegram
app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ativo!")

app.add_handler(CommandHandler("start", start))

app.run_polling()
