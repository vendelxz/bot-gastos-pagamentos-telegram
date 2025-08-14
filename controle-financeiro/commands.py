from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, CommandHandler, filters
from database import add_usuario, get_usuario, add_gasto, get_gastos, get_resumo, get_cartoes, get_categorias, add_cartao
from pdf_generator import gerar_pdf

# Estados do fluxo
STATE_VALOR = "aguardando_valor"
STATE_NOVO_CARTAO = "aguardando_novo_cartao"

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
    teclado = [[InlineKeyboardButton(cat['nome'], callback_data=f"categoria|{cat['nome']}")] for cat in categorias]
    await update.message.reply_text("Escolha a categoria do gasto:", reply_markup=InlineKeyboardMarkup(teclado))

async def callback_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    categoria = query.data.split("|")[1]
    context.user_data['categoria'] = categoria
    context.user_data['state'] = STATE_VALOR
    await query.message.reply_text("Agora envie o valor do gasto (somente números):")

async def valor_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') != STATE_VALOR:
        return

    texto = update.message.text.replace(",", ".")
    if not texto.replace(".", "").isdigit():
        await update.message.reply_text("Valor inválido. Envie apenas números.")
        return

    valor = float(texto)
    context.user_data['valor'] = valor
    context.user_data['state'] = None  # reset do estado de valor

    usuario = get_usuario(update.effective_user.id)
    cartoes = get_cartoes(usuario['id'])

    teclado = [[InlineKeyboardButton(c['nome'], callback_data=f"cartao|{c['id']}")] for c in cartoes]
    teclado.append([InlineKeyboardButton("Adicionar novo cartão", callback_data="cartao|novo")])
    teclado.append([InlineKeyboardButton("Em dinheiro", callback_data="cartao|0")])
    await update.message.reply_text("Escolha o cartão ou forma de pagamento:", reply_markup=InlineKeyboardMarkup(teclado))

async def callback_cartao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cartao_id = query.data.split("|")[1]
    usuario = get_usuario(update.effective_user.id)

    if cartao_id == "novo":
        context.user_data['state'] = STATE_NOVO_CARTAO
        await query.message.reply_text("Digite o nome do novo cartão:")
        return

    if cartao_id == "0":
        add_gasto(usuario['id'], "Dinheiro", None, context.user_data['categoria'], context.user_data['valor'])
        await query.message.reply_text(f"Gasto de R$ {context.user_data['valor']:.2f} registrado em dinheiro.")
    else:
        add_gasto(usuario['id'], "Cartão", int(cartao_id), context.user_data['categoria'], context.user_data['valor'])
        await query.message.reply_text(f"Gasto de R$ {context.user_data['valor']:.2f} registrado no cartão.")

    context.user_data.clear()

async def novo_cartao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') != STATE_NOVO_CARTAO:
        return

    nome_cartao = update.message.text.strip()
    usuario = get_usuario(update.effective_user.id)
    add_cartao(usuario['id'], nome_cartao)
    add_gasto(usuario['id'], "Cartão", None, context.user_data['categoria'], context.user_data['valor'])
    await update.message.reply_text(f"Cartão '{nome_cartao}' adicionado e gasto registrado com R$ {context.user_data['valor']:.2f}.")
    context.user_data.clear()

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, novo_cartao))
