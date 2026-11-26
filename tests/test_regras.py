from datetime import date
from unittest.mock import Mock
import pytest
from confeitaria.regras import (
    MENSAGEM_SEM_PEDIDOS_PENDENTES,
    MENSAGEM_SEM_VENDAS_MES,
    ordenar_menos_vendidos_mes,
    preparar_pedidos_pendentes,
)

from confeitaria.regras import (
    EnviadorDeEmail,
    PedidoAtraso,
    ProcessadorDePedidos,
    RelogioDoSistema,
    RepositorioDePedidos,
    calcular_preco_com_desconto_atraso,
    calcular_preco_com_status_entrega,
)
from confeitaria.regras import MENSAGEM_SEM_DOCES, preparar_precos_doces

def test_produto_entregue_no_dia_recebe_dois_por_cento():
    assert calcular_preco_com_status_entrega(100.0, "no_dia") == 102.0


def test_produto_valor_zero_com_bonus():
    assert calcular_preco_com_status_entrega(0.0, "no_dia") == 0.0


def test_produto_entregue_antes_do_prazo_nao_recebe_bonus():
    assert calcular_preco_com_status_entrega(200.0, "antes") == 200.0


def test_produto_entregue_com_atraso_nao_recebe_bonus():
    assert calcular_preco_com_status_entrega(200.0, "atrasado") == 200.0


def test_recusa_preco_negativo_no_bonus():
    with pytest.raises(ValueError):
        calcular_preco_com_status_entrega(-50.0, "no_dia")


def test_desconto_atraso_zero_dias():
    assert calcular_preco_com_desconto_atraso(200.0, 0) == 200.0


def test_desconto_atraso_um_dia():
    assert calcular_preco_com_desconto_atraso(200.0, 1) == 199.0


def test_desconto_atraso_quatro_dias():
    assert calcular_preco_com_desconto_atraso(200.0, 4) == 196.0


def test_recusa_dias_atraso_negativos():
    with pytest.raises(ValueError):
        calcular_preco_com_desconto_atraso(200.0, -1)


def test_pedido_atrasado_envia_email_de_aviso():
    pedido_atrasado = PedidoAtraso(
        id_pedido=1,
        cliente_email="cliente@email.com",
        data_prevista=date(2026, 11, 10),
    )
    repositorio = Mock(spec=RepositorioDePedidos)
    repositorio.buscar_pendentes.return_value = [pedido_atrasado]
    enviador_email = Mock(spec=EnviadorDeEmail)
    relogio = Mock(spec=RelogioDoSistema)
    relogio.hoje.return_value = date(2026, 11, 15)

    processador = ProcessadorDePedidos(repositorio, enviador_email, relogio)
    processador.processar_atrasados()

    assert processador.total_notificados == 1
    enviador_email.enviar.assert_called_once_with(
        "cliente@email.com",
        "O seu pedido #1 está atrasado!",
    )


def test_pedido_no_prazo_nao_envia_email():
    pedido_no_prazo = PedidoAtraso(
        id_pedido=2,
        cliente_email="cliente@email.com",
        data_prevista=date(2026, 11, 20),
    )
    repositorio = Mock(spec=RepositorioDePedidos)
    repositorio.buscar_pendentes.return_value = [pedido_no_prazo]
    enviador_email = Mock(spec=EnviadorDeEmail)
    relogio = Mock(spec=RelogioDoSistema)
    relogio.hoje.return_value = date(2026, 11, 15)

    processador = ProcessadorDePedidos(repositorio, enviador_email, relogio)
    processador.processar_atrasados()

    assert processador.total_notificados == 0
    enviador_email.enviar.assert_not_called()

def test_menos_vendidos_retorna_aviso_quando_vazio_ou_sem_vendas():
    assert ordenar_menos_vendidos_mes([]) == MENSAGEM_SEM_VENDAS_MES
    assert ordenar_menos_vendidos_mes([("Bolo Chocolate", 0), ("Torta Limão", 0)]) == MENSAGEM_SEM_VENDAS_MES


def test_menos_vendidos_ordena_crescente_com_zero_no_topo():
    dados = [("Brigadeiro", 5), ("Torta Limão", 0), ("Bolo Chocolate", 2)]
    assert ordenar_menos_vendidos_mes(dados) == [
        ("Torta Limão", 0),
        ("Bolo Chocolate", 2),
        ("Brigadeiro", 5),
    ]


def test_pedidos_pendentes_filtra_ordena_e_avisa_quando_vazio():
    assert preparar_pedidos_pendentes([]) == MENSAGEM_SEM_PEDIDOS_PENDENTES
    assert (
        preparar_pedidos_pendentes([{"id": 1, "data_entregue": "2026-11-20", "data_prevista": "2026-11-20"}])
        == MENSAGEM_SEM_PEDIDOS_PENDENTES
    )

    pedidos = [
        {"id": 10, "cliente": "Ana", "data_prevista": "2026-11-28", "data_entregue": None},
        {"id": 11, "cliente": "Bruno", "data_entregue": "2026-11-24", "data_prevista": "2026-11-25"},
        {"id": 12, "cliente": "Carla", "data_prevista": "2026-11-26", "data_entregue": None},
    ]
    resultado = preparar_pedidos_pendentes(pedidos)
    assert [p["id"] for p in resultado] == [12, 10]

def test_preparar_precos_doces_vazio_ou_sem_ativos():
    assert preparar_precos_doces([]) == MENSAGEM_SEM_DOCES
    assert (
        preparar_precos_doces(
            [{"nome_doce": "Bolo - Chocolate", "preco": 45.0, "ativo": False}]
        )
        == MENSAGEM_SEM_DOCES
    )


def test_preparar_precos_doces_filtra_inativos_e_formata_preco():
    itens = [
        {"nome_doce": "Torta - Limão", "preco": 38.5, "ativo": True},
        {"nome_doce": "Bolo - Chocolate", "preco": 45.0, "ativo": False},
        {"nome_doce": "Brigadeiro - Tradicional", "preco": 4.0, "ativo": True},
    ]
    assert preparar_precos_doces(itens) == [
        {"nome_doce": "Brigadeiro - Tradicional", "preco_unitario": "R$ 4,00"},
        {"nome_doce": "Torta - Limão", "preco_unitario": "R$ 38,50"},
    ]