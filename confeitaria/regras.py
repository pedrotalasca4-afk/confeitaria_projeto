from datetime import date
MENSAGEM_SEM_VENDAS_MES = "nenhuma venda este mês"
MENSAGEM_SEM_PEDIDOS_PENDENTES = "nenhum pedido pendente"

def calcular_preco_com_status_entrega(preco: float, status_entrega: str) -> float:
    """Calcula o preço com base nos três estados de entrega:
    - 'antes': entregue antes do prazo (sem bônus)
    - 'no_dia': entregue exatamente na data prevista (recebe 2% de bônus)
    - 'atrasado': entregue com atraso (sem bônus)
    """
    if preco < 0:
        raise ValueError("Não se aceita preço negativo")
    if status_entrega == "no_dia":
        return round(preco * 1.02, 2)
    if status_entrega in ("antes", "atrasado"):
        return round(preco, 2)
    raise ValueError("Status de entrega inválido")


def calcular_preco_com_desconto_atraso(preco: float, dias_atraso: int) -> float:
    """Aplica desconto de 0,5% por dia de atraso (acumulativo)."""
    if preco < 0:
        raise ValueError("Não se aceita preço negativo")
    if dias_atraso < 0:
        raise ValueError("Dias de atraso não podem ser negativos")
    desconto_total = dias_atraso * 0.005
    return round(preco * (1 - desconto_total), 2)


class PedidoAtraso:
    def __init__(
        self,
        id_pedido: int,
        cliente_email: str,
        data_prevista: date,
        data_entregue: date | None = None,
    ):
        self.id_pedido = id_pedido
        self.cliente_email = cliente_email
        self.data_prevista = data_prevista
        self.data_entregue = data_entregue

    def atrasado_em(self, hoje: date) -> bool:
        return self.data_entregue is None and hoje > self.data_prevista


class RepositorioDePedidos:
    def buscar_pendentes(self) -> list[PedidoAtraso]:
        raise NotImplementedError("Conecta no PostgreSQL em produção")


class EnviadorDeEmail:
    def enviar(self, destinatario: str, mensagem: str) -> None:
        raise NotImplementedError("Implementado pela camada de notificação/interface")


class RelogioDoSistema:
    def hoje(self) -> date:
        return date.today()


class ProcessadorDePedidos:
    def __init__(self, repositorio_pedidos, enviador_email, relogio):
        self.repositorio_pedidos = repositorio_pedidos
        self.enviador_email = enviador_email
        self.relogio = relogio
        self.total_notificados = 0

    def processar_atrasados(self) -> None:
        hoje = self.relogio.hoje()
        for pedido in self.repositorio_pedidos.buscar_pendentes():
            if pedido.atrasado_em(hoje):
                self.enviador_email.enviar(
                    pedido.cliente_email,
                    f"O seu pedido #{pedido.id_pedido} está atrasado!",
                )
                self.total_notificados += 1

def ordenar_menos_vendidos_mes(itens: list[tuple[str,int]]) -> list[tuple[str,int]] | str:
    """Recebe lista de (nome_tipo_doce, quantidade_no_mes).
    Retorna 'nenhuma venda este mês' se não houver itens ou se todas as contagens forem 0.
    Caso contrário, retorna ordenado de forma crescente (0 vendas primeiro).
    """
    if not itens:
        return MENSAGEM_SEM_VENDAS_MES
    
    total_vendas = sum(qtd for _, qtd in itens)
    if total_vendas == 0:
        return MENSAGEM_SEM_VENDAS_MES
    
    return sorted(itens, key=lambda item: (item[1], item[0].lower()))

def preparar_pedidos_pendentes(pedidos: list[dict]) -> list[dict] | str:
    """Filtra pedidos pendentes (sem data_entregue), ordena por data_prevista
    e devolve 'nenhum pedido pendente' quando não houver nenhum.
    """
    pendentes = [p for p in pedidos if p.get("data_entregue") is None]
    if not pendentes:
        return MENSAGEM_SEM_PEDIDOS_PENDENTES
    
    return sorted(pendentes, key=lambda p: str(p.get("data_prevista", "")))