from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Access(C3DInstruction):
    def __init__(self, stack_heap, position, line, column):
        super().__init__(line, column)
        self.stack_heap = stack_heap
        self.position: C3DInstruction = position

    def get_code(self):
        return str(self.stack_heap) + '[int(' + self.position.get_code() + ')]'