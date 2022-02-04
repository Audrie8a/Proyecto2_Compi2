from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Function(C3DInstruction):
    def __init__(self, instr, id, line, column):
        super().__init__(line, column)
        self.instr = instr
        self.id = id

    def get_code(self):
        ret = f'func {self.id}(){{\n'
        for ins in self.instr:
            auxText = ins.get_code()
            if auxText == '':
                continue
            ret = ret + f'\t{auxText}'
            if ins.isLeader:
                ret = ret + '\t\t\t\t\t\t\t// Lider'
            ret = ret + '\n'
        ret = ret + '}'
        return ret