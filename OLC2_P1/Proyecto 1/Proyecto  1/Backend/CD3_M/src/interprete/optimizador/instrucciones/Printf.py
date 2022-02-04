from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Printf(C3DInstruction):
    def __init__(self, str_to, exp, line, column):
        super().__init__(line, column)
        self.str_to = str_to
        self.exp = exp

    def get_code(self):
        return (
            'fmt.Printf(' + self.str_to + ', int(' + self.exp.get_code() + '));'
        )