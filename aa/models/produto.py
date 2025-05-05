class Produto:
    def __init__(self, codproduto, nome, preco):
        self.codproduto = codproduto
        self.nome = nome
        self.preco = preco

    def __repr__(self):
        return f"Produto({self.codproduto}, {self.nome}, {self.preco})"
