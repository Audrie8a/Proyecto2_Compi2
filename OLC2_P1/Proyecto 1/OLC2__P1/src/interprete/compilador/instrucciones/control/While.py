from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class While(Instruccion):
    def __init__(self, condition, instruccions, line, column):
        super().__init__(line, column)
        self.condition: Instruccion = condition
        self.inst_list: Instruccion = instruccions
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        self.generador.begin_comment('WHILE')
        new_env = Entorno(entorno)
        # L0: While
        lb_wh = self.generador.new_label()
        self.generador.set_label(lb_wh)
        condition: Valor = self.condition.compilar(entorno)

        if condition.get_type() != TipoVar.BOOLEAN:
            self.generador.new_error(
                'Error, la condicion no es de tipo boolean', self.line, self.column
            )
            return
        new_env.set_break(condition.get_false_label())
        new_env.set_continue(lb_wh)
        # L1: True label
        self.generador.set_label(condition.get_true_label())
        self.inst_list.compilar(new_env)

        # Regresar al while
        self.generador.new_goto(lb_wh)
        # L2: False label
        self.generador.set_label(condition.get_false_label())

        self.generador.end_comment('FIN WHILE')

    def set_labels(self):
        return super().set_labels()