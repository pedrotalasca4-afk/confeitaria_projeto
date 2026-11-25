import pytest
from confeitaria.conexao import obter_conexao_teste


@pytest.fixture
def conexao():
    conn = obter_conexao_teste()
    cursor = conn.cursor()
    cursor.execute(
        "TRUNCATE solicitacao, item_pedido, pedido, doce, tipo_doce, "
        "cliente_telefone, cliente RESTART IDENTITY CASCADE;"
    )
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()