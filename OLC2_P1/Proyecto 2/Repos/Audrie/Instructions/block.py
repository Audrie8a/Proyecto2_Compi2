from Abstract.Instruction import Instruction


class block(Instruction):
    def __init__(self, instructions, line, column) -> None:
        super().__init__()
        self.instructions = instructions
        self.line=line
        self.column = column

    def compile (self, environment):
        for ins in self.instructions:
            ret = ins.compile(environment)