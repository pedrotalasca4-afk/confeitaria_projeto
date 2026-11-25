import os
import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()


def _montar_config(usar_banco_teste: bool = False) -> dict:
    host = os.getenv("PG_HOST", "localhost")
    porta = int(os.getenv("PG_PORTA", "5432"))
    usuario = os.getenv("PG_USUARIO")
    senha = os.getenv("PG_SENHA")
    variavel_banco = "PG_BANCO_DE_TESTE" if usar_banco_teste else "PG_BANCO"
    banco_padrao = "confeitaria_teste" if usar_banco_teste else "confeitaria"
    banco = os.getenv(variavel_banco, banco_padrao)

    faltando = [
        nome
        for nome, valor in [
            ("PG_USUARIO", usuario),
            ("PG_SENHA", senha),
            (variavel_banco, banco),
        ]
        if not valor
    ]
    if faltando:
        raise RuntimeError(
            f"Variáveis de ambiente ausentes no .env ou sistema: {', '.join(faltando)}. "
            "Copie o .env.exemplo para .env e preencha os dados."
        )

    return {
        "host": host,
        "port": porta,
        "user": usuario,
        "password": senha,
        "dbname": banco,
    }


def obter_conexao():
    """Abre conexão para o banco principal da aplicação (PG_BANCO)."""
    return pg.connect(**_montar_config(usar_banco_teste=False))


def obter_conexao_teste():
    """Abre conexão para o banco isolado de testes (PG_BANCO_DE_TESTE)."""
    return pg.connect(**_montar_config(usar_banco_teste=True))