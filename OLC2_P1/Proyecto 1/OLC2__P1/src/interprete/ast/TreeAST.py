from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.simbolos.Entorno import Entorno


class TreeAST(Instruccion):
    def __init__(self, inst_list, line, column):
        super().__init__(0, 0)
        self.inst_list = inst_list
        self.entorno: Entorno = None
        self.code = ''
        self.error_list = []

    def compilar(self, entorno: Entorno):
        self.entorno = entorno
        for inst in self.inst_list:
            inst: Instruccion
            inst.compilar(self.entorno)

    def set_labels(self):
        pass