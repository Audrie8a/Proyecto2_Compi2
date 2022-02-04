from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Literal(C3DInstruction):
    def __init__(self, value, line, column, constant=False):
        super().__init__(line, column)
        self.value = value
        self.constant = constant

    def get_code(self):
        return str(self.value)