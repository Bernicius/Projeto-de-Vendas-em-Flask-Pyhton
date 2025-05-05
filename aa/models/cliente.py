class Cliente:
    def __init__(self, codcliente, nome, endereco):
        self.codcliente = codcliente
        self.nome = nome
        self.endereco = endereco

    def __repr__(self):
        return f"Cliente({self.codcliente}, {self.nome}, {self.endereco})"
