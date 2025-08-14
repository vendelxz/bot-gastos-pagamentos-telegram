from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def gerar_pdf(nome_usuario, gastos):
    data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"gastos_{nome_usuario}_{data_atual}.pdf"
    caminho = os.path.join("pdfs", nome_arquivo)

    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    doc = SimpleDocTemplate(caminho, pagesize=A4)
    elementos = []
    styles = getSampleStyleSheet()

    titulo = Paragraph(f"<b>Relatório de Gastos - {nome_usuario}</b>", styles['Title'])
    data_geracao = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    elementos.extend([titulo, data_geracao, Spacer(1, 20)])

    # Cabeçalho da tabela
    tabela_dados = [["Data", "Categoria", "Tipo de Pagamento", "Valor (R$)"]]

    total_geral = 0
    for gasto in gastos:
        data_gasto = gasto.get("data")
        if isinstance(data_gasto, datetime):
            data_gasto = data_gasto.strftime("%d/%m/%Y")
        categoria = gasto.get("categoria", "Sem categoria")
        tipo_pagamento = gasto.get("tipo_pagamento", "Desconhecido")
        valor = gasto.get("valor", 0)
        total_geral += valor
        tabela_dados.append([data_gasto, categoria, tipo_pagamento, f"{valor:.2f}"])

    # Adiciona linha de total
    tabela_dados.append(["", "", "<b>Total</b>", f"<b>{total_geral:.2f}</b>"])

    tabela = Table(tabela_dados, colWidths=[80, 150, 100, 80])
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
