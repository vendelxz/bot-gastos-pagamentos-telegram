from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
from database import get_usuario, get_gastos_para_pdf

def gerar_pdf_mes(telegram_id, mes, ano):
    usuario = get_usuario(telegram_id)
    if not usuario:
        return None

    gastos = get_gastos_para_pdf(usuario['id'], mes, ano)
    if not gastos:
        return None

    data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"gastos_{usuario['nome']}_{mes}_{ano}_{data_atual}.pdf"
    caminho = os.path.join("pdfs", nome_arquivo)
    os.makedirs("pdfs", exist_ok=True)

    doc = SimpleDocTemplate(caminho, pagesize=A4)
    elementos = []
    styles = getSampleStyleSheet()

    titulo = Paragraph(f"<b>Relatório de Gastos - {usuario['nome']} - {mes}/{ano}</b>", styles['Title'])
    data_geracao = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    elementos.extend([titulo, data_geracao, Spacer(1, 20)])

    tabela_dados = [["Data", "Categoria", "Tipo de Pagamento", "Cartão", "Valor (R$)"]]
    total_geral = 0

    for g in gastos:
        data_gasto = g["data_gasto"].strftime("%d/%m/%Y") if isinstance(g["data_gasto"], datetime) else g["data_gasto"]
        categoria = g["categoria"] or "Sem categoria"
        tipo_pagamento = g["tipo_pagamento"]
        cartao = g["cartao"] or "Dinheiro"
        valor = g["valor"]
        total_geral += valor
        tabela_dados.append([data_gasto, categoria, tipo_pagamento, cartao, f"{valor:.2f}"])

    tabela_dados.append(["", "", "", "<b>Total</b>", f"<b>{total_geral:.2f}</b>"])
    tabela = Table(tabela_dados, colWidths=[80, 150, 100, 100, 80])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-2), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (-2,-1), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (-2,-1), (-1,-1), 'RIGHT'),
    ]))

    elementos.append(tabela)
    doc.build(elementos)
    return caminho
