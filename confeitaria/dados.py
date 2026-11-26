import psycopg2 as pg


class Cliente:
    def __init__(
        self,
        nome: str,
        logradouro: str,
        numero: int,
        bairro: str,
        cidade: str,
        cep: str,
        id_cliente: int | None = None,
    ):
        self.id_cliente = id_cliente
        self.nome = nome
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep

    def __str__(self) -> str:
        return (
            f"Cliente(id={self.id_cliente}, nome='{self.nome}', "
            f"endereco='{self.logradouro}, {self.numero} - {self.bairro}, "
            f"{self.cidade} ({self.cep})')"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ClienteTelefone:
    def __init__(self, id_cliente: int, numero: str, id_telefone: int | None = None):
        self.id_telefone = id_telefone
        self.id_cliente = id_cliente
        self.numero = numero

    def __str__(self) -> str:
        return (
            f"ClienteTelefone(id={self.id_telefone}, "
            f"id_cliente={self.id_cliente}, numero='{self.numero}')"
        )

    def __repr__(self) -> str:
        return self.__str__()


class TipoDoce:
    def __init__(self, sabor: str, tipo: str, id_tipo: int | None = None):
        self.id_tipo = id_tipo
        self.sabor = sabor
        self.tipo = tipo

    def __str__(self) -> str:
        return f"TipoDoce(id={self.id_tipo}, tipo='{self.tipo}', sabor='{self.sabor}')"

    def __repr__(self) -> str:
        return self.__str__()


class Doce:
    def __init__(self, id_tipo: int, preco: float, id_doce: int | None = None):
        self.id_doce = id_doce
        self.id_tipo = id_tipo
        self.preco = preco

    def __str__(self) -> str:
        return f"Doce(id={self.id_doce}, id_tipo={self.id_tipo}, preco=R${self.preco:.2f})"

    def __repr__(self) -> str:
        return self.__str__()


class Pedido:
    def __init__(
        self,
        data_feita: str,
        data_prevista: str,
        data_entregue: str | None = None,
        id_pedido: int | None = None,
    ):
        self.id_pedido = id_pedido
        self.data_feita = data_feita
        self.data_prevista = data_prevista
        self.data_entregue = data_entregue

    def __str__(self) -> str:
        return (
            f"Pedido(id={self.id_pedido}, feita='{self.data_feita}', "
            f"prevista='{self.data_prevista}', entregue='{self.data_entregue}')"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ItemPedido:
    def __init__(
        self,
        id_pedido: int,
        id_doce: int,
        id_cliente: int,
        total_pago: float,
        troco: float,
    ):
        self.id_pedido = id_pedido
        self.id_doce = id_doce
        self.id_cliente = id_cliente
        self.total_pago = total_pago
        self.troco = troco

    def __str__(self) -> str:
        return (
            f"ItemPedido(pedido={self.id_pedido}, doce={self.id_doce}, "
            f"cliente={self.id_cliente}, pago=R${self.total_pago:.2f}, troco=R${self.troco:.2f})"
        )

    def __repr__(self) -> str:
        return self.__str__()


class Solicitacao:
    def __init__(self, id_cliente: int, id_pedido: int):
        self.id_cliente = id_cliente
        self.id_pedido = id_pedido

    def __str__(self) -> str:
        return f"Solicitacao(id_cliente={self.id_cliente}, id_pedido={self.id_pedido})"

    def __repr__(self) -> str:
        return self.__str__()


# --- Cliente ---
def criar_cliente(
    conexao,
    nome: str,
    logradouro: str,
    numero: int,
    bairro: str,
    cidade: str,
    cep: str,
) -> Cliente | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO cliente (nome, logradouro, numero, bairro, cidade, cep) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_cliente;",
            (nome, logradouro, numero, bairro, cidade, cep),
        )
        id_cliente = cursor.fetchone()[0]
        conexao.commit()
        return Cliente(nome, logradouro, numero, bairro, cidade, cep, id_cliente=id_cliente)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_clientes(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM cliente ORDER BY id_cliente;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_cliente(
    conexao,
    id_cliente: int,
    novo_logradouro: str,
    novo_numero: int,
    novo_bairro: str,
    nova_cidade: str,
    novo_cep: str,
) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE cliente SET logradouro = %s, numero = %s, bairro = %s, "
            "cidade = %s, cep = %s WHERE id_cliente = %s;",
            (novo_logradouro, novo_numero, novo_bairro, nova_cidade, novo_cep, id_cliente),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_cliente(conexao, id_cliente: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s;", (id_cliente,))
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- ClienteTelefone ---
def criar_telefone(conexao, id_cliente: int, numero: str) -> ClienteTelefone | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO cliente_telefone (id_cliente, numero) VALUES (%s, %s) RETURNING id_telefone;",
            (id_cliente, numero),
        )
        id_telefone = cursor.fetchone()[0]
        conexao.commit()
        return ClienteTelefone(id_cliente, numero, id_telefone=id_telefone)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_telefones(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM cliente_telefone ORDER BY id_telefone;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_telefone(conexao, id_telefone: int, novo_numero: str) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE cliente_telefone SET numero = %s WHERE id_telefone = %s;",
            (novo_numero, id_telefone),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_telefone(conexao, id_telefone: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM cliente_telefone WHERE id_telefone = %s;", (id_telefone,))
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- TipoDoce ---
def criar_tipo_doce(conexao, sabor: str, tipo: str) -> TipoDoce | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO tipo_doce (sabor, tipo) VALUES (%s, %s) RETURNING id_tipo;",
            (sabor, tipo),
        )
        id_tipo = cursor.fetchone()[0]
        conexao.commit()
        return TipoDoce(sabor, tipo, id_tipo=id_tipo)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_tipos_doce(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM tipo_doce ORDER BY id_tipo;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_tipo_doce(conexao, id_tipo: int, novo_sabor: str, novo_tipo: str) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE tipo_doce SET sabor = %s, tipo = %s WHERE id_tipo = %s;",
            (novo_sabor, novo_tipo, id_tipo),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_tipo_doce(conexao, id_tipo: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM tipo_doce WHERE id_tipo = %s;", (id_tipo,))
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- Doce ---
def criar_doce(conexao, id_tipo: int, preco: float) -> Doce | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO doce (id_tipo, preco) VALUES (%s, %s) RETURNING id_doce;",
            (id_tipo, preco),
        )
        id_doce = cursor.fetchone()[0]
        conexao.commit()
        return Doce(id_tipo, preco, id_doce=id_doce)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_doces(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM doce ORDER BY id_doce;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_doce(conexao, id_doce: int, novo_preco: float) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE doce SET preco = %s WHERE id_doce = %s;",
            (novo_preco, id_doce),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_doce(conexao, id_doce: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM doce WHERE id_doce = %s;", (id_doce,))
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- Pedido ---
def criar_pedido(
    conexao,
    data_feita: str,
    data_prevista: str,
    data_entregue: str | None = None,
) -> Pedido | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO pedido (data_feita, data_prevista, data_entregue) "
            "VALUES (%s, %s, %s) RETURNING id_pedido;",
            (data_feita, data_prevista, data_entregue),
        )
        id_pedido = cursor.fetchone()[0]
        conexao.commit()
        return Pedido(data_feita, data_prevista, data_entregue, id_pedido=id_pedido)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_pedidos(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM pedido ORDER BY id_pedido;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_pedido(conexao, id_pedido: int, nova_data_entregue: str) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE pedido SET data_entregue = %s WHERE id_pedido = %s;",
            (nova_data_entregue, id_pedido),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_pedido(conexao, id_pedido: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM pedido WHERE id_pedido = %s;", (id_pedido,))
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- ItemPedido ---
def criar_item_pedido(
    conexao,
    id_pedido: int,
    id_doce: int,
    id_cliente: int,
    total_pago: float,
    troco: float,
) -> ItemPedido | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO item_pedido (id_pedido, id_doce, id_cliente, total_pago, troco) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id_pedido, id_doce, id_cliente;",
            (id_pedido, id_doce, id_cliente, total_pago, troco),
        )
        resultado = cursor.fetchone()
        conexao.commit()
        return ItemPedido(resultado[0], resultado[1], resultado[2], total_pago, troco)
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_itens_pedido(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM item_pedido ORDER BY id_pedido, id_doce;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_item_pedido(
    conexao,
    id_pedido: int,
    id_doce: int,
    id_cliente: int,
    novo_total_pago: float,
    novo_troco: float,
) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE item_pedido SET total_pago = %s, troco = %s "
            "WHERE id_pedido = %s AND id_doce = %s AND id_cliente = %s;",
            (novo_total_pago, novo_troco, id_pedido, id_doce, id_cliente),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_item_pedido(conexao, id_pedido: int, id_doce: int, id_cliente: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "DELETE FROM item_pedido WHERE id_pedido = %s AND id_doce = %s AND id_cliente = %s;",
            (id_pedido, id_doce, id_cliente),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


# --- Solicitacao ---
def criar_solicitacao(conexao, id_cliente: int, id_pedido: int) -> Solicitacao | None:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO solicitacao (id_cliente, id_pedido) VALUES (%s, %s) "
            "RETURNING id_cliente, id_pedido;",
            (id_cliente, id_pedido),
        )
        resultado = cursor.fetchone()
        conexao.commit()
        return Solicitacao(resultado[0], resultado[1])
    except pg.DatabaseError:
        conexao.rollback()
        return None


def ler_solicitacoes(conexao) -> list[tuple]:
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM solicitacao ORDER BY id_cliente, id_pedido;")
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        return []


def atualizar_solicitacao(
    conexao,
    id_cliente_atual: int,
    id_pedido_atual: int,
    novo_id_cliente: int,
    novo_id_pedido: int,
) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "UPDATE solicitacao SET id_cliente = %s, id_pedido = %s "
            "WHERE id_cliente = %s AND id_pedido = %s;",
            (novo_id_cliente, novo_id_pedido, id_cliente_atual, id_pedido_atual),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False


def deletar_solicitacao(conexao, id_cliente: int, id_pedido: int) -> bool:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "DELETE FROM solicitacao WHERE id_cliente = %s AND id_pedido = %s;",
            (id_cliente, id_pedido),
        )
        conexao.commit()
        return cursor.rowcount > 0
    except pg.DatabaseError:
        conexao.rollback()
        return False
    
def listar_tipos_doce_menos_vendidos_mes(conexao, ano: int, mes: int) -> list[tuple[str, int]]:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            SELECT
                CONCAT(td.tipo, ' - ', td.sabor) AS nome_doce,
                COUNT(ip.id_pedido) AS total_vendas
            FROM tipo_doce td
            LEFT JOIN doce d
                ON d.id_tipo = td.id_tipo
            LEFT JOIN item_pedido ip
                ON ip.id_doce = d.id_doce
            LEFT JOIN pedido p
                ON p.id_pedido = ip.id_pedido
               AND EXTRACT(YEAR FROM p.data_feita) = %s
               AND EXTRACT(MONTH FROM p.data_feita) = %s
            GROUP BY td.id_tipo, td.tipo, td.sabor
            ORDER BY total_vendas ASC, nome_doce ASC;
            """,
            (ano, mes),
        )
        return cursor.fetchall()
    except pg.DatabaseError:
        conexao.rollback()
        raise


def listar_pedidos_pendentes_detalhados(conexao) -> list[dict]:
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            SELECT
                p.id_pedido,
                COALESCE(c.nome, 'Cliente não informado') AS cliente,
                STRING_AGG(CONCAT(td.tipo, ' ', td.sabor), ', ' ORDER BY td.tipo, td.sabor) AS doces,
                p.data_prevista,
                p.data_entregue
            FROM pedido p
            LEFT JOIN solicitacao s
                ON s.id_pedido = p.id_pedido
            LEFT JOIN cliente c
                ON c.id_cliente = COALESCE(s.id_cliente, (
                    SELECT ip2.id_cliente
                    FROM item_pedido ip2
                    WHERE ip2.id_pedido = p.id_pedido
                    LIMIT 1
                ))
            LEFT JOIN item_pedido ip
                ON ip.id_pedido = p.id_pedido
            LEFT JOIN doce d
                ON d.id_doce = ip.id_doce
            LEFT JOIN tipo_doce td
                ON td.id_tipo = d.id_tipo
            WHERE p.data_entregue IS NULL
            GROUP BY p.id_pedido, c.nome, p.data_prevista, p.data_entregue
            ORDER BY p.data_prevista ASC, p.id_pedido ASC;
            """,
        )
        linhas = cursor.fetchall()
        return [
            {
                "id_pedido": linha[0],
                "cliente": linha[1],
                "doces": linha[2] or "Sem itens",
                "data_prevista": linha[3],
                "data_entregue": linha[4],
            }
            for linha in linhas
        ]
    except pg.DatabaseError:
        conexao.rollback()
        raise

def listar_precos_tipos_doce(conexao) -> list[dict]:
    """Lista tipos de doce ativos com seu respectivo preço unitário."""
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
            SELECT
                CONCAT(td.tipo, ' - ', td.sabor) AS nome_doce,
                d.preco,
                COALESCE(td.ativo, TRUE) AS ativo
            FROM tipo_doce td
            INNER JOIN doce d
                ON d.id_tipo = td.id_tipo
            WHERE COALESCE(td.ativo, TRUE) IS TRUE
            ORDER BY td.tipo ASC, td.sabor ASC, d.id_doce ASC;
            """
        )
        linhas = cursor.fetchall()
        return [
            {
                "nome_doce": linha[0],
                "preco": linha[1],
                "ativo": linha[2],
            }
            for linha in linhas
        ]
    except pg.DatabaseError:
        conexao.rollback()
        raise