from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Return(C3DInstruction):
    def __init__(self, line, column):
        super().__init__(line, column)

    def get_code(self):
        return 'return;'