# MoneyControl 💰

**MoneyControl** é um bot do Telegram para controle financeiro pessoal e familiar.  
Ele permite registrar gastos por cartão ou dinheiro, organizar por categorias, gerar resumos mensais e criar PDFs detalhados com os gastos.  
Ideal para acompanhar suas finanças de forma prática, rápida e segura.

---

## 🚀 Funcionalidades
- Registrar gastos por categoria e tipo de pagamento (`/gasto`)  
- Visualizar resumo mensal de gastos (`/resumo`)  
- Gerar PDF detalhado com gastos do mês (`/pdf`)  
- Cadastro de usuários automaticamente via Telegram (`/start`)  
- Cadastro e gerenciamento de cartões de forma dinâmica  

---

## ⚙️ Tecnologias utilizadas
- **Python 3.12**  
- [python-telegram-bot](https://python-telegram-bot.org/) – integração com Telegram  
- [ReportLab](https://www.reportlab.com/) – geração de PDFs  
- [PostgreSQL](https://www.postgresql.org/) via [Neon](https://neon.tech/) – armazenamento de dados  

---

## 📌 Observações importantes
- As tabelas `usuarios`, `cartoes`, `categorias` e `gastos` devem existir no banco e estar corretamente configuradas.  
- `telegram_id` em `usuarios` deve ser **único** para evitar erros no comando `/start`.  
- Novos cartões são cadastrados automaticamente durante o fluxo de gasto, garantindo que o gasto seja registrado corretamente.  
- PDFs são gerados na pasta `pdfs` e enviados diretamente pelo Telegram.  

---

## 👤 Autor
José Wendel
