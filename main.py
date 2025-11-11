import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass

# ===============================
# Red-Black Tree (inserção, remoção, busca)
# ===============================

@dataclass(eq=False)  # importante p/ usar _Node como chave de dict (hash por identidade)
class _Node:
    key: str
    data: dict
    color: str = "RED"   # "RED" ou "BLACK"
    left:  "._Node" = None
    right: "._Node" = None
    parent: "._Node" = None


class RedBlackTree:
    def __init__(self):
        self.NULL = _Node(key=None, data=None, color="BLACK")
        self.NULL.left = self.NULL.right = self.NULL.parent = self.NULL
        self.root = self.NULL

    # ---------- Utilidades ----------
    def _transplant(self, u: _Node, v: _Node):
        """Substitui o subárvore enraizado em u pelo de v (clássico de BST)."""
        if u.parent == self.NULL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x: _Node):
        while x.left != self.NULL:
            x = x.left
        return x

    # ---------- Rotações ----------
    def _left_rotate(self, x: _Node):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NULL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: _Node):
        y = x.left
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NULL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # ---------- Inserção ----------
    def insert(self, key: str, data: dict):
        key = str(key)
        z = _Node(key=key, data=data, color="RED",
                  left=self.NULL, right=self.NULL, parent=self.NULL)

        y = self.NULL
        x = self.root
        while x != self.NULL:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key > x.key:
                x = x.right
            else:
                # chave já existe -> atualizar conteúdo e sair
                x.data = data
                return

        z.parent = y
        if y == self.NULL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._insert_fixup(z)

    def _insert_fixup(self, z: _Node):
        # Casos 1,2,3 e versões espelhadas (conforme slide de referência)
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # tio
                if y.color == "RED":
                    # Caso 1: tio vermelho -> recoloração e sobe
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Caso 2: triângulo (dir) -> rot. esquerda para virar caso 3
                        z = z.parent
                        self._left_rotate(z)
                    # Caso 3: linha (esq) -> recoloração + rot. direita
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._right_rotate(z.parent.parent)
            else:
                # espelho: troca left<->right
                y = z.parent.parent.left
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._left_rotate(z.parent.parent)
        self.root.color = "BLACK"

    # ---------- Remoção ----------
    def delete(self, key: str) -> bool:
        """Remove a chave se existir. Retorna True se removeu, False se não encontrou."""
        key = str(key)
        z = self._find_node(key)
        if z is None:
            return False

        y = z
        y_original_color = y.color
        if z.left == self.NULL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NULL:
            x = z.left
            self._transplant(z, z.left)
        else:
            # sucessor
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._delete_fixup(x)
        return True

    def _delete_fixup(self, x: _Node):
        # Trata "duplo-preto" em x até restaurar as propriedades
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right  # irmão
                if w.color == "RED":
                    # Caso 1: irmão vermelho
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    # Caso 2: irmão preto com dois filhos pretos
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        # Caso 3: irmão preto, filho esquerdo vermelho, direito preto
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right
                    # Caso 4: irmão preto, filho direito vermelho
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                # espelho: troca left<->right
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"

    # ---------- Busca/Travessias ----------
    def _find_node(self, key: str):
        key = str(key)
        x = self.root
        while x != self.NULL:
            if key == x.key:
                return x
            x = x.left if key < x.key else x.right
        return None

    def search(self, key: str):
        return self._find_node(key)

    def inorder(self):
        res = []
        def _in(n):
            if n == self.NULL: return
            _in(n.left)
            res.append((n.key, n.data, n.color))
            _in(n.right)
        _in(self.root)
        return res


# ===============================
# GUI (Tkinter + ttk)
# ===============================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Livros — Árvore Rubro-Negra (IME/USP-style)")
        self.root.geometry("1040x680")
        self.root.minsize(940, 580)

        self.tree = RedBlackTree()
        self._make_style()
        self._build_layout()
        self._seed_examples()

    def _make_style(self):
        style = ttk.Style(self.root)
        try:
            if "vista" in style.theme_names():
                style.theme_use("vista")
            else:
                style.theme_use("clam")
        except Exception:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", font=("Segoe UI", 11))
        style.configure("Card.TFrame", background="#ffffff", borderwidth=1, relief="solid")
        style.configure("Header.TFrame", background="#0e1116")
        style.configure("Header.TLabel", background="#0e1116", foreground="#e6edf3", font=("Segoe UI", 14, "bold"))
        style.configure("Accent.TButton", padding=8)

    def _build_layout(self):
        # Header
        header = ttk.Frame(self.root, style="Header.TFrame")
        header.pack(side="top", fill="x")
        ttk.Label(header, text="Catálogo de Livros • RB-Tree (Inserção+Remoção com fix-ups)", style="Header.TLabel").pack(side="left", padx=16, pady=10)

        # Body
        body = ttk.Frame(self.root, padding=14)
        body.pack(fill="both", expand=True)

        # Sidebar (form + busca + remover)
        sidebar = ttk.Frame(body)
        sidebar.pack(side="left", fill="y", padx=(0,14))

        # Card: Adicionar/Atualizar
        card1 = ttk.Frame(sidebar, padding=12, style="Card.TFrame")
        card1.pack(fill="x")
        ttk.Label(card1, text="Adicionar / Atualizar", style="Title.TLabel").pack(anchor="w")
        ttk.Label(card1, text="(ISBN é a chave da RB-Tree)", style="Sub.TLabel").pack(anchor="w", pady=(0,8))

        frm = ttk.Frame(card1)
        frm.pack(fill="x")

        self.var_isbn = tk.StringVar()
        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_ano = tk.StringVar()

        def add_row(parent, r, label, var, width=34):
            ttk.Label(parent, text=label).grid(row=r, column=0, sticky="w", pady=4)
            e = ttk.Entry(parent, textvariable=var, width=width)
            e.grid(row=r, column=1, sticky="we", pady=4)
            parent.columnconfigure(1, weight=1)
            return e

        add_row(frm, 0, "ISBN", self.var_isbn)
        add_row(frm, 1, "Título", self.var_titulo)
        add_row(frm, 2, "Autor", self.var_autor)
        add_row(frm, 3, "Ano", self.var_ano, width=12)

        btns = ttk.Frame(card1)
        btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text="Salvar (INSERIR/ATUALIZAR)", style="Accent.TButton", command=self._on_save).pack(side="left")
        ttk.Button(btns, text="Limpar", command=lambda: [v.set("") for v in (self.var_isbn, self.var_titulo, self.var_autor, self.var_ano)]).pack(side="left", padx=8)

        # Card: Buscar
        card2 = ttk.Frame(sidebar, padding=12, style="Card.TFrame")
        card2.pack(fill="x", pady=14)
        ttk.Label(card2, text="Buscar por ISBN", style="Title.TLabel").pack(anchor="w")
        frm_b = ttk.Frame(card2)
        frm_b.pack(fill="x", pady=(6,0))
        self.var_busca = tk.StringVar()
        ttk.Label(frm_b, text="ISBN").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frm_b, textvariable=self.var_busca, width=28).grid(row=0, column=1, sticky="we", pady=4)
        ttk.Button(card2, text="Buscar", command=self._on_search).pack(anchor="w", pady=(8,0))

        # Card: Remover
        card3 = ttk.Frame(sidebar, padding=12, style="Card.TFrame")
        card3.pack(fill="x")
        ttk.Label(card3, text="Remover por ISBN", style="Title.TLabel").pack(anchor="w")
        frm_r = ttk.Frame(card3)
        frm_r.pack(fill="x", pady=(6,0))
        self.var_remove = tk.StringVar()
        ttk.Label(frm_r, text="ISBN").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frm_r, textvariable=self.var_remove, width=28).grid(row=0, column=1, sticky="we", pady=4)
        ttk.Button(card3, text="Remover", command=self._on_remove).pack(anchor="w", pady=(8,0))

        # Main content (Notebook)
        main = ttk.Notebook(body)
        main.pack(side="left", fill="both", expand=True)

        # Aba catálogo (lista em-ordem)
        self.tab_list = ttk.Frame(main, padding=12)
        main.add(self.tab_list, text="Catálogo (em-ordem)")

        self.treeview = ttk.Treeview(self.tab_list, columns=("isbn","titulo","autor","ano","cor"), show="headings", height=14)
        self.treeview.heading("isbn", text="ISBN")
        self.treeview.heading("titulo", text="Título")
        self.treeview.heading("autor", text="Autor")
        self.treeview.heading("ano", text="Ano")
        self.treeview.heading("cor", text="Cor do Nó")
        self.treeview.column("isbn", width=140, stretch=False)
        self.treeview.column("titulo", width=280)
        self.treeview.column("autor", width=180)
        self.treeview.column("ano", width=60, anchor="center")
        self.treeview.column("cor", width=90, anchor="center")
        self.treeview.pack(fill="both", expand=True)

        # Aba árvore (visual)
        self.tab_tree = ttk.Frame(main, padding=12)
        main.add(self.tab_tree, text="Visualização da Árvore")

        # Canvas com scroll + pan + zoom
        container = ttk.Frame(self.tab_tree)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, background="#ffffff", highlightthickness=1, highlightbackground="#d0d7de")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scy = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scx = ttk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scy.set, xscrollcommand=scx.set)
        scy.grid(row=0, column=1, sticky="ns")
        scx.grid(row=1, column=0, sticky="ew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Pan/Zoom
        self._scale = 1.0
        self.canvas.bind("<ButtonPress-1>", self._scan_start)
        self.canvas.bind("<B1-Motion>", self._scan_move)
        self.canvas.bind("<MouseWheel>", self._on_wheel)  # Windows
        self.canvas.bind("<Button-4>", self._on_wheel)    # Linux
        self.canvas.bind("<Button-5>", self._on_wheel)    # Linux
        ttk.Button(self.tab_tree, text="Recentrar/Redesenhar", command=self._redraw).pack(pady=8)

        # Rodapé
        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x")
        ttk.Label(footer, text="Dica: arraste com botão esquerdo (pan) | Rodinha do mouse (zoom) | Clique no botão para recentrar").pack(padx=12, pady=6)

        self._refresh_list()
        self._redraw()

    # ---------- Ações ----------
    def _on_save(self):
        isbn = self.var_isbn.get().strip()
        titulo = self.var_titulo.get().strip()
        autor = self.var_autor.get().strip() or "—"
        ano = self.var_ano.get().strip()

        if not isbn or not titulo:
            messagebox.showerror("Campos obrigatórios", "Informe ao menos ISBN e Título.")
            return

        try:
            ano_int = int(ano) if ano else None
        except ValueError:
            messagebox.showerror("Valor inválido", "O campo Ano deve ser numérico.")
            return

        livro = {"isbn": str(isbn), "titulo": titulo, "autor": autor, "ano": ano_int}
        self.tree.insert(livro["isbn"], livro)
        self._refresh_list()
        self._redraw()
        messagebox.showinfo("Sucesso", "Livro inserido/atualizado.")

    def _on_search(self):
        isbn = (self.var_busca.get() or "").strip()
        if not isbn:
            messagebox.showwarning("Busca", "Informe o ISBN para buscar.")
            return
        node = self.tree.search(isbn)
        if node:
            livro = node.data
            messagebox.showinfo("Encontrado",
                                f"ISBN: {livro['isbn']}\nTítulo: {livro['titulo']}\nAutor: {livro['autor']}\nAno: {livro['ano']}\nCor do nó: {node.color}")
        else:
            messagebox.showerror("Não encontrado", "Nenhum livro com esse ISBN.")

    def _on_remove(self):
        isbn = (self.var_remove.get() or "").strip()
        if not isbn:
            messagebox.showwarning("Remoção", "Informe o ISBN para remover.")
            return
        ok = self.tree.delete(isbn)
        if ok:
            self._refresh_list()
            self._redraw()
            messagebox.showinfo("Remoção", f"Livro {isbn} removido.")
        else:
            messagebox.showerror("Remoção", "ISBN não encontrado.")

    # ---------- Lista em-ordem ----------
    def _refresh_list(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        for key, data, color in self.tree.inorder():
            self.treeview.insert("", "end", values=(data["isbn"], data["titulo"], data["autor"], data["ano"], color))

    # ---------- Visualização da Árvore ----------
    def _scan_start(self, e):
        self.canvas.scan_mark(e.x, e.y)

    def _scan_move(self, e):
        self.canvas.scan_dragto(e.x, e.y, gain=1)

    def _on_wheel(self, e):
        if hasattr(e, "delta") and e.delta != 0:
            factor = 1.1 if e.delta > 0 else 1/1.1
        else:
            factor = 1.1 if getattr(e, "num", 5) == 4 else 1/1.1
        self._scale *= factor
        self._draw_tree()

    def _redraw(self):
        self._scale = 1.0
        self._draw_tree()

    def _positions(self):
        # X pela travessia em-ordem; Y pela profundidade
        order = []
        def inorder(n, depth=0):
            if n == self.tree.NULL: return
            inorder(n.left, depth+1)
            order.append(n)
            inorder(n.right, depth+1)
        inorder(self.tree.root, 0)
        x_index = {n: i for i, n in enumerate(order)}

        coords = {}
        def assign(n, depth=0):
            if n == self.tree.NULL: return
            x = x_index[n] * 140
            y = depth * 120
            coords[n] = (x, y)
            assign(n.left, depth+1)
            assign(n.right, depth+1)
        assign(self.tree.root, 0)
        return coords

    def _draw_tree(self):
        c = self.canvas
        c.delete("all")
        root = self.tree.root
        if root == self.tree.NULL:
            c.create_text(20, 20, anchor="nw", text="Árvore vazia. Insira livros para visualizar.", font=("Segoe UI", 11))
            return

        coords = self._positions()
        if not coords:
            return

        xs = [x for x, y in coords.values()]
        ys = [y for x, y in coords.values()]
        pad = 240
        c.config(scrollregion=(min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad))

        # Arestas
        for n, (x, y) in coords.items():
            for child in (n.left, n.right):
                if child != self.tree.NULL and child in coords:
                    cx, cy = coords[child]
                    c.create_line(x, y, cx, cy, width=2, fill="#9aa4b2")

        # Nós
        for n, (x, y) in coords.items():
            r = int(22 * self._scale)
            fill = "#d43333" if n.color == "RED" else "#1f2328"
            outline = "#8b0000" if n.color == "RED" else "#111417"
            c.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2)
            key_txt = n.key if isinstance(n.key, str) else str(n.key)
            c.create_text(x, y, fill="#ffffff", text=key_txt[:7], font=("Segoe UI", max(9, int(10*self._scale)), "bold"))

        # Legenda
        c.create_rectangle(10, 10, 240, 70, fill="#ffffff", outline="#d0d7de")
        c.create_oval(20, 20, 40, 40, fill="#d43333", outline="#8b0000", width=2)
        c.create_text(50, 30, text="Vermelho", anchor="w")
        c.create_oval(130, 20, 150, 40, fill="#1f2328", outline="#111417", width=2)
        c.create_text(160, 30, text="Preto", anchor="w")

    # ---------- Dados de exemplo ----------
    def _seed_examples(self):
        exemplos = [
            {"isbn":"970783","titulo":"O Pequeno Príncipe","autor":"Antoine de Saint-Exupéry","ano":1943},
            {"isbn":"978184","titulo":"Dom Casmurro","autor":"Machado de Assis","ano":1899},
            {"isbn":"978467","titulo":"Grande Sertão: Veredas","autor":"J. G. Rosa","ano":1956},
            {"isbn":"978076","titulo":"Vidas Secas","autor":"Graciliano Ramos","ano":1938},
            {"isbn":"978825","titulo":"Capitães da Areia","autor":"Jorge Amado","ano":1937},
            {"isbn":"978628","titulo":"Torto Arado","autor":"Itamar Vieira Jr.","ano":2019},
            {"isbn":"978651","titulo":"Quarto de Despejo","autor":"Carolina Maria de Jesus","ano":1960},
        ]
        for l in exemplos:
            self.tree.insert(l["isbn"], l)
        self._refresh_list()
        self._redraw()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
