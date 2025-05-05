class Venda:
    def __init__(self, codvenda, data, valor_total, codcliente):
        self.codvenda = codvenda
        self.data = data
        self.valor_total = valor_total
        self.codcliente = codcliente

    def __repr__(self):
        return f"Venda({self.codvenda}, {self.data}, {self.valor_total}, {self.codcliente})"
