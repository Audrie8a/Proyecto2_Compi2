from src.interprete.optimizador.C3DInstruction import C3DInstruction


class IF(C3DInstruction):
    def __init__(self, condition, label, line, column):
        super().__init__(line, column)
        self.condition: C3DInstruction = condition
        self.label = label

    def get_code(self):
        return (
            'if ('
            + self.condition.get_code()
            + ') { goto'
            + str(self.label)
            + '; }'
        )