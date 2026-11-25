from confeitaria.dados import (
    atualizar_cliente,
    criar_cliente,
    deletar_cliente,
    ler_clientes,
)

from confeitaria.dados import (
    criar_cliente,
    criar_doce,
    criar_item_pedido,
    criar_pedido,
    criar_solicitacao,
    criar_tipo_doce,
    listar_pedidos_pendentes_detalhados,
    listar_tipos_doce_menos_vendidos_mes,
)


def test_criar_e_ler_cliente(conexao):
    cliente = criar_cliente(
        conexao,
        "Ana Clara",
        "Rua das Flores",
        100,
        "Centro",
        "Porto Alegre",
        "90010-000",
    )
    assert cliente is not None
    assert cliente.id_cliente is not None

    clientes = ler_clientes(conexao)
    assert len(clientes) == 1
    assert clientes[0][0] == cliente.id_cliente


def test_atualizar_cliente(conexao):
    cliente = criar_cliente(
        conexao,
        "Bruno Silva",
        "Av. Brasil",
        200,
        "Floresta",
        "Porto Alegre",
        "90230-060",
    )
    atualizado = atualizar_cliente(
        conexao,
        cliente.id_cliente,
        "Av. Ipiranga",
        500,
        "Partenon",
        "Porto Alegre",
        "90610-001",
    )
    assert atualizado is True

    clientes = ler_clientes(conexao)
    assert clientes[0][2] == "Av. Ipiranga"
    assert clientes[0][3] == 500


def test_deletar_cliente(conexao):
    cliente = criar_cliente(
        conexao,
        "Carla Souza",
        "Rua Ramiro Barcelos",
        300,
        "Bom Fim",
        "Porto Alegre",
        "90035-007",
    )
    removido = deletar_cliente(conexao, cliente.id_cliente)
    assert removido is True
    assert ler_clientes(conexao) == []


def test_banco_recusa_dado_invalido(conexao):
    invalido = criar_cliente(
        conexao,
        None,
        "Rua Sem Nome",
        10,
        "Centro",
        "Porto Alegre",
        "90000-000",
    )
    assert invalido is None

def test_listar_tipos_doce_menos_vendidos_mes_inclui_zero_vendas(conexao):
    td_torta = criar_tipo_doce(conexao, "Limão", "Torta")
    td_bolo = criar_tipo_doce(conexao, "Chocolate", "Bolo")
    cliente = criar_cliente(conexao, "Ana", "Rua A", 10, "Centro", "Porto Alegre", "90010-000")
    doce_bolo = criar_doce(conexao, td_bolo.id_tipo, 45.0)
    pedido = criar_pedido(conexao, "2026-11-10", "2026-11-12", "2026-11-12")
    criar_solicitacao(conexao, cliente.id_cliente, pedido.id_pedido)
    criar_item_pedido(conexao, pedido.id_pedido, doce_bolo.id_doce, cliente.id_cliente, 45.0, 0.0)

    resultado = listar_tipos_doce_menos_vendidos_mes(conexao, 2026, 11)
    assert ("Torta - Limão", 0) in resultado
    assert ("Bolo - Chocolate", 1) in resultado


def test_listar_pedidos_pendentes_detalhados_ignora_entregues(conexao):
    td = criar_tipo_doce(conexao, "Morango", "Torta")
    cliente = criar_cliente(conexao, "João", "Rua B", 20, "Centro", "Porto Alegre", "90020-000")
    doce = criar_doce(conexao, td.id_tipo, 50.0)

    pendente = criar_pedido(conexao, "2026-11-20", "2026-11-26", None)
    criar_solicitacao(conexao, cliente.id_cliente, pendente.id_pedido)
    criar_item_pedido(conexao, pendente.id_pedido, doce.id_doce, cliente.id_cliente, 50.0, 0.0)

    entregue = criar_pedido(conexao, "2026-11-15", "2026-11-18", "2026-11-18")
    criar_solicitacao(conexao, cliente.id_cliente, entregue.id_pedido)

    pendentes = listar_pedidos_pendentes_detalhados(conexao)
    assert len(pendentes) == 1
    assert pendentes[0]["id_pedido"] == pendente.id_pedido
    assert pendentes[0]["cliente"] == "João"