class ItemVenda:
    def __init__(self, codvenda, codproduto, qtde, valor):
        self.codvenda = codvenda
        self.codproduto = codproduto
        self.qtde = qtde
        self.valor = valor

    def __repr__(self):
        return f"ItemVenda({self.codvenda}, {self.codproduto}, {self.qtde}, {self.valor})"
