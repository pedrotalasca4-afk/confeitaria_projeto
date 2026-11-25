from confeitaria.conexao import obter_conexao
from confeitaria.janela import JanelaConfeitaria


def main() -> None:
    conexao = obter_conexao()
    try:
        app = JanelaConfeitaria(conexao)
        app.mainloop()
    finally:
        conexao.close()


if __name__ == "__main__":
    main()