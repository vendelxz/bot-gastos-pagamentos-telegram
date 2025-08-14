from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import add_usuario, get_usuario, add_gasto, get_gastos, get_resumo, get_cartoes, get_categorias
from pdf_generator import gerar_pdf
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    nome = update.effective_user.first_name
    add_usuario(telegram_id, nome)
    await update.message.reply_text(
        f"Olá {nome}! Eu sou o MoneyControl 💰\n"
        "Comandos disponíveis:\n"
        "/gasto - registrar gasto\n"
        "/resumo - ver resumo do mês\n"
        "/pdf - gerar PDF com gastos"
    )

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    usuario = get_usuario(telegram_id)
    if not usuario:
        await update.message.reply_text("Usuário não cadastrado.")
        return

    categorias = get_categorias()
    teclado = [
        [InlineKeyboardButton(cat['nome'], callback_data=f"categoria|{cat['nome']}")] for cat in categorias
    ]
    await update.message.reply_text("Escolha a categoria do gasto:", reply_markup=InlineKeyboardMarkup(teclado))

async def callback_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    categoria = query.data.split("|")[1]
    context.user_data['categoria'] = categoria
    await query.message.reply_text(f"Categoria selecionada: {categoria}\nAgora envie o valor do gasto (somente números):")

async def valor_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.replace(",", ".")
    if not texto.replace(".", "").isdigit():
        await update.message.reply_text("Valor inválido. Envie apenas números.")
        return
    valor = float(texto)
    context.user_data['valor'] = valor
    usuario = get_usuario(update.effective_user.id)
    cartoes = get_cartoes(usuario['id'])
    if cartoes:
        teclado = [
            [InlineKeyboardButton(cartao['nome'], callback_data=f"cartao|{cartao['id']}")] for cartao in cartoes
        ]
        teclado.append([InlineKeyboardButton("Em dinheiro", callback_data="cartao|0")])
        await update.message.reply_text("Escolha o cartão ou dinheiro:", reply_markup=InlineKeyboardMarkup(teclado))
    else:
        add_gasto(usuario['id'], "Dinheiro", None, context.user_data['categoria'], valor)
        await update.message.reply_text(f"Gasto de R$ {valor:.2f} registrado em dinheiro.")

async def callback_cartao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cartao_id = int(query.data.split("|")[1])
    usuario = get_usuario(update.effective_user.id)
    add_gasto(usuario['id'], "Cartão" if cartao_id != 0 else "Dinheiro", cartao_id if cartao_id != 0 else None, context.user_data['categoria'], context.user_data['valor'])
    await query.message.reply_text(f"Gasto de R$ {context.user_data['valor']:.2f} registrado com sucesso.")

async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = get_usuario(update.effective_user.id)
    gastos = get_resumo(usuario['id'])
    if not gastos:
        await update.message.reply_text("Nenhum gasto registrado ainda.")
        return
    texto = "Resumo de gastos:\n"
    for g in gastos:
        texto += f"{g['categoria']} ({g['tipo_pagamento']}): R$ {g['total']:.2f}\n"
    await update.message.reply_text(texto)

async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = get_usuario(update.effective_user.id)
    gastos = get_gastos(usuario['id'])
    if not gastos:
        await update.message.reply_text("Nenhum gasto registrado para gerar PDF.")
        return
    caminho = gerar_pdf(usuario['nome'], gastos)
    with open(caminho, "rb") as file:
        await update.message.reply_document(file)

def registrar_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gasto", gasto))
    app.add_handler(CommandHandler("resumo", resumo))
    app.add_handler(CommandHandler("pdf", pdf))
    app.add_handler(CallbackQueryHandler(callback_categoria, pattern="^categoria\\|"))
    app.add_handler(CallbackQueryHandler(callback_cartao, pattern="^cartao\\|"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, valor_gasto))
