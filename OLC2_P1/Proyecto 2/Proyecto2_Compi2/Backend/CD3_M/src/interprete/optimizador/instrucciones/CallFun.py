from src.interprete.optimizador.C3DInstruction import C3DInstruction


class CallFun(C3DInstruction):
    def __init__(self, id, line, column):
        super().__init__(line, column)
        self.id = id

    def get_code(self):
        return f'{self.id}();'