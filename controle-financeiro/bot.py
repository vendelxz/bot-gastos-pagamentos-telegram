# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN
from server import start_server

# Funções de comando
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou o MoneyControl 💰\n"
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

# Inicia servidor HTTP em background
start_server()

# Configuração do bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gasto", gasto))
app.add_handler(CommandHandler("resumo", resumo))
app.add_handler(CommandHandler("pdf", pdf))

print("Bot rodando...")
app.run_polling()
