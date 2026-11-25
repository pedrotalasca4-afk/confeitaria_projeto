from confeitaria.conexao import obter_conexao
from confeitaria.dados import ler_clientes


def main() -> None:
    conexao = obter_conexao()
    try:
        clientes = ler_clientes(conexao)
        print(f"Conexão ativa. Clientes cadastrados: {len(clientes)}")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()