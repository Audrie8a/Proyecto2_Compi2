from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Expression(C3DInstruction):
    def __init__(self, left, right, type_of, line, column, constant=False):
        super().__init__(line, column)
        self.left: C3DInstruction = left
        self.right: C3DInstruction = right
        self.type_of = type_of
        self.constant = left.constant or right.constant

    def neutral_ops(self):
        if self.type_of == '+' or self.type_of == '-':
            self.deleted = (
                self.right.get_code() == '0' or self.left.get_code() == '0'
            )
        elif self.type_of == '*':
            self.deleted = (
                self.right.get_code() == '1' or self.left.get_code() == '1'
            )
        elif self.type_of == '/':
            self.deleted = self.right.get_code() == '1'
        return self.deleted

    def get_contrary(self):
        if self.type_of == '>':
            self.type_of = '<='
        elif self.type_of == '<':
            self.type_of = '>='
        elif self.type_of == '>=':
            self.type_of = '<'
        elif self.type_of == '<=':
            self.type_of = '>'
        elif self.type_of == '==':
            self.type_of = '!='
        elif self.type_of == '!=':
            self.type_of = '=='
        else:
            self.type_of = ''

    def get_code(self):
        return (
            str(self.left.get_code())
            + ' '
            + self.type_of
            + ' '
            + str(self.right.get_code())
        )