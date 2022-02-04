from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Statement(Instruccion):
    def __init__(self, list_inst, line, column):
        super().__init__(line, column)
        self.ints_list = list_inst

    def compilar(self, entorno: Entorno):
        try:
            for inst in self.ints_list:
                inst.compilar(entorno)
        except Exception:
            print(Exception)
            print('Error al compilar lista de instrucciones')
            self.generador.new_error(
                'Error al compilar lista de instrucciones',
                self.line,
                self.column,
            )
            return

    def set_labels(self):
        pass