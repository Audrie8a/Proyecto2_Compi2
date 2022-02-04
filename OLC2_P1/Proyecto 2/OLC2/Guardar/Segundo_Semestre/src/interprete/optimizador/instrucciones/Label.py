from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Label(C3DInstruction):
    def __init__(self, id, line, column):
        self.id = id
        self.isLeader = True

    def get_code(self):
        if self.deleted:
            return ''
        return f'{self.id}:'