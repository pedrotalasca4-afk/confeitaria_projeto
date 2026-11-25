import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2 as pg

from confeitaria import dados, regras


class JanelaConfeitaria(tk.Tk):
    def __init__(self, conexao):
        super().__init__()
        self.conexao = conexao
        self.title("Confeitaria - Aula 03")
        self.geometry("760x440")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_menos_vendidos = ttk.Frame(notebook)
        self.aba_pendentes = ttk.Frame(notebook)

        notebook.add(self.aba_menos_vendidos, text="Menos vendidos no mês")
        notebook.add(self.aba_pendentes, text="Pedidos pendentes")

        self._montar_aba_menos_vendidos()
        self._montar_aba_pendentes()
        self.atualizar_tudo()

    def _montar_aba_menos_vendidos(self):
        topo = ttk.Frame(self.aba_menos_vendidos)
        topo.pack(fill="x", pady=(0, 8))

        ttk.Label(topo, text="Ano:").pack(side="left")
        self.campo_ano = ttk.Entry(topo, width=8)
        self.campo_ano.insert(0, "2026")
        self.campo_ano.pack(side="left", padx=(4, 12))

        ttk.Label(topo, text="Mês:").pack(side="left")
        self.campo_mes = ttk.Entry(topo, width=5)
        self.campo_mes.insert(0, "11")
        self.campo_mes.pack(side="left", padx=(4, 12))

        ttk.Button(topo, text="Atualizar", command=self.carregar_menos_vendidos).pack(side="left")

        self.aviso_vendas = ttk.Label(self.aba_menos_vendidos, text="")
        self.aviso_vendas.pack(anchor="w", pady=(0, 4))

        self.tabela_vendas = ttk.Treeview(
            self.aba_menos_vendidos,
            columns=("tipo_doce", "quantidade"),
            show="headings",
        )
        self.tabela_vendas.heading("tipo_doce", text="Tipo de Doce")
        self.tabela_vendas.heading("quantidade", text="Vendas no Mês")
        self.tabela_vendas.pack(fill="both", expand=True)

    def _montar_aba_pendentes(self):
        topo = ttk.Frame(self.aba_pendentes)
        topo.pack(fill="x", pady=(0, 8))
        ttk.Button(topo, text="Atualizar pendentes", command=self.carregar_pendentes).pack(side="left")

        self.aviso_pendentes = ttk.Label(self.aba_pendentes, text="")
        self.aviso_pendentes.pack(anchor="w", pady=(0, 4))

        self.tabela_pendentes = ttk.Treeview(
            self.aba_pendentes,
            columns=("pedido", "cliente", "doces", "data_prevista"),
            show="headings",
        )
        self.tabela_pendentes.heading("pedido", text="Pedido #")
        self.tabela_pendentes.heading("cliente", text="Cliente")
        self.tabela_pendentes.heading("doces", text="Doces")
        self.tabela_pendentes.heading("data_prevista", text="Data Prevista")
        self.tabela_pendentes.pack(fill="both", expand=True)

    def carregar_menos_vendidos(self):
        for item in self.tabela_vendas.get_children():
            self.tabela_vendas.delete(item)
        self.aviso_vendas.config(text="")

        try:
            ano = int(self.campo_ano.get().strip())
            mes = int(self.campo_mes.get().strip())
        except ValueError:
            messagebox.showwarning("Confira os dados", "Informe ano e mês numéricos válidos.")
            return

        try:
            brutos = dados.listar_tipos_doce_menos_vendidos_mes(self.conexao, ano, mes)
        except pg.DatabaseError as erro:
            messagebox.showerror("Erro no banco", f"Falha ao consultar vendas do mês: {erro}")
            return

        resultado = regras.ordenar_menos_vendidos_mes(brutos)
        if isinstance(resultado, str):
            self.aviso_vendas.config(text=resultado)
            messagebox.showinfo("Aviso", resultado)
            return

        for nome_doce, qtd in resultado:
            self.tabela_vendas.insert("", "end", values=(nome_doce, qtd))

    def carregar_pendentes(self):
        for item in self.tabela_pendentes.get_children():
            self.tabela_pendentes.delete(item)
        self.aviso_pendentes.config(text="")

        try:
            brutos = dados.listar_pedidos_pendentes_detalhados(self.conexao)
        except pg.DatabaseError as erro:
            messagebox.showerror("Erro no banco", f"Falha ao consultar pedidos pendentes: {erro}")
            return

        resultado = regras.preparar_pedidos_pendentes(brutos)
        if isinstance(resultado, str):
            self.aviso_pendentes.config(text=resultado)
            messagebox.showinfo("Aviso", resultado)
            return

        for p in resultado:
            self.tabela_pendentes.insert(
                "",
                "end",
                values=(p["id_pedido"], p["cliente"], p["doces"], p["data_prevista"]),
            )

    def atualizar_tudo(self):
        self.carregar_menos_vendidos()
        self.carregar_pendentes()