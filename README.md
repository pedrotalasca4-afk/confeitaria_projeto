# Confeitaria

Sistema de apoio à gestão da confeitaria com camadas separadas de regras de negócio, acesso a dados em PostgreSQL e interface gráfica em Tkinter.

## O problema
A confeitaria precisa acompanhar quais tipos de doces são menos vendidos no mês (incluindo os com 0 vendas) para ajustar a produção e evitar desperdício, além de visualizar rapidamente os pedidos pendentes de entrega com cliente, doces e data prevista.

## Estrutura do projeto
- `banco/`: scripts SQL das tabelas.
- `confeitaria/`: conexão com o banco, regras (`regras.py`), dados (`dados.py`) e interface (`janela.py`).
- `tests/`: testes unitários e de integração com `pytest`.
- `main.py`: ponto de entrada que abre a janela e gerencia a conexão.
- `.env.exemplo`: modelo de variáveis de ambiente.

## Como configurar e rodar
1. Instale as dependências:
   ```powershell
   pip install -r requirements.txt