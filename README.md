# MoneyControl 💰

**MoneyControl** é um bot do Telegram para controle financeiro pessoal e familiar, desenvolvido para rodar localmente no seu computador.
Ele permite registrar gastos por cartão ou dinheiro, organizar por categorias, gerar resumos mensais e criar PDFs detalhados com os gastos.
Ideal para acompanhar suas finanças de forma prática, rápida e segura, sem depender de serviços na nuvem.

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
- [PostgreSQL](https://www.postgresql.org/) – armazenamento de dados
- [Docker] para rodar o Bot localmente sem a necessidade de servidor 

---

## 📌 Observações importantes
- As tabelas `usuarios`, `cartoes`, `categorias` e `gastos` devem existir no banco e estar corretamente configuradas.  
- `telegram_id` em `usuarios` deve ser **único** para evitar erros no comando `/start`.  
- Novos cartões são cadastrados automaticamente durante o fluxo de gasto, garantindo que o gasto seja registrado corretamente.  
- PDFs são gerados na pasta `pdfs` e enviados diretamente pelo Telegram.  

---
## 📌 Pendências e Melhorias

- [ ] **Geração de PDF**  
  - Mesmo com gastos registrados, o PDF retorna "não há gastos registrados".  
  - Corrigir a busca e leitura dos dados antes da geração.

- [ ] **Cadastro de Cartões**  
  - Cartões não estão sendo salvos no banco de dados, impedindo o processamento de gastos associados a eles.  
  - Adicionar opção, ao cadastrar um cartão, de escolher entre já existentes ou inserir um novo.

- [ ] **Resumo de Gastos**  
  - Atualmente exibe apenas a lista de gastos.  
  - Adicionar soma total no final do resumo.

- [ ] **Organização por Mês**  
  - Criar forma de filtrar gastos por mês.  
  - Banco de dados poderia "esvaziar" automaticamente ao iniciar um novo mês, evitando acúmulo excessivo de dados.

- [ ] **Descrição dos Gastos**  
  - Permitir inserir uma descrição detalhada junto à categoria.  
  - Exemplo: `Contas - "Esse é o gasto com aluguel"`.

- [ ] **Forma de Pagamento (Pix)**  
  - Adicionar opção de pagamento via Pix no cadastro de gastos.
---

## 👤 Autor
José Wendel
