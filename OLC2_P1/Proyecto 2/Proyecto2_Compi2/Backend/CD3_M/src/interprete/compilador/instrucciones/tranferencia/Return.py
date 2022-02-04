from src.interprete.compilador.simbolos.SimboloFuncion import SimboloFuncion
from src.interprete.compilador.tipos.Tipo import TipoVar, get_tipo_var
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Return(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(line, column)
        self.expresion: Instruccion = expresion
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):

        value: Valor = (
            self.expresion.compilar(entorno)
            if self.expresion
            else Valor('0', TipoVar.VOID, False)
        )
        funct_simbol: SimboloFuncion = entorno.get_now_function()
        if funct_simbol is None:
            self.generador.new_error(
                'Return fuera de funcion', self.line, self.column
            )
            return

        if funct_simbol.get_type() != value.get_type():
            error_ = (
                'El tipo "'
                + get_tipo_var(value.get_type())
                + '" no es asignable al tipo "'
                + get_tipo_var(funct_simbol.get_type())
                + '"'
            )
            self.generador.new_error(error_, self.line, self.column)
            return

        if value.get_type() == TipoVar.BOOLEAN:
            tmp_lb = self.generador.new_label()

            self.generador.set_label(value.get_true_label())
            self.generador.set_stack('P', '1')
            self.generador.new_goto(tmp_lb)

            self.generador.set_label(value.get_false_label())
            self.generador.set_stack('P', '0')

            self.generador.set_label(tmp_lb)
        else:
            if value.get_type() != TipoVar.VOID:
                self.generador.set_stack('P', value.get_value())

        self.generador.new_goto(entorno.get_return())

    def set_labels(self):
        pass