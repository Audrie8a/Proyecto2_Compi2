from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Continue(Instruccion):
    def __init__(self, line, column):
        super().__init__(line, column)
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        if entorno.get_break() is None:
            self.generador.new_error(
                'El continue solo puede estar en instrucciones de tipo ciclo',
                self.line,
                self.column,
            )
            return
        self.generador.new_goto(entorno.get_continue())

    def set_labels(self):
        pass