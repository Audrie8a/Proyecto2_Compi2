from src.interprete.optimizador.expresiones.Literal import Literal
from src.interprete.optimizador.C3DInstruction import C3DInstruction


class Assignment(C3DInstruction):
    def __init__(self, place, exp, line, column):
        super().__init__(line, column)
        self.place: C3DInstruction = place
        self.exp = exp

    def self_assignment(self):
        aux = None
        if isinstance(self.exp, Literal):
            aux = self.place.get_code() == self.exp.get_code()
        else:
            aux = (
                self.place.get_code() == self.exp.right.get_code()
                or self.place.get_code() == self.exp.left.get_code()
            )
        return aux

    def get_code(self):
        if self.deleted:
            return ''
        return self.place.get_code() + ' = ' + self.exp.get_code() + ';'