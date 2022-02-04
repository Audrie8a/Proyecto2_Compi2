from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.simbolos.Simbolo import Simbolo
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class AccesoVariable(Instruccion):
    def __init__(self, id, line, column):
        super().__init__(line, column)
        self.id = id
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        self.generador.new_comment_line()
        self.generador.new_commnet(f'Acceso a variable: {self.id}')

        var_simbol: Simbolo = entorno.get_variable(self.id)
        if var_simbol is None:
            self.end_commnet()
            self.generador.new_error(
                f'No existe la variable "{self.id}"', self.line, self.column
            )
            return

        # Tempral para guardar la variable
        tmp_var = self.generador.new_temp()
        # Obtencion de la posicion de la variable
        tmp_pos = var_simbol.get_position()

        if not var_simbol.get_is_global():
            tmp_pos = self.generador.new_temp()
            # self.generador.free_temp(tmp_pos)  # FIXME: Revisar
            self.generador.new_exp(
                tmp_pos,
                'P',
                var_simbol.get_position(),
                '+',
                'Posicionar el puntero',
            )
        self.generador.get_stack(tmp_var, tmp_pos)

        if var_simbol.get_type() != TipoVar.BOOLEAN:
            self.end_commnet()
            valor_return = Valor(tmp_var, var_simbol.get_type(), True)
            if var_simbol.get_type() == TipoVar.ARRAY:
                valor_return.set_aux_type(var_simbol.get_tipo_aux())
            return valor_return

        # self.generador.free_temp(tmp_var)  # FIXME: REVISAR
        self.set_labels()

        self.generador.new_if(tmp_var, '1', '==', self.true_label)
        self.generador.new_goto(self.false_label)

        ret_value = Valor(None, TipoVar.BOOLEAN, False)
        ret_value.set_true_label(self.true_label)
        ret_value.set_false_label(self.false_label)
        self.end_commnet()
        return ret_value

    def set_labels(self):
        if self.true_label == '':
            self.true_label = self.generador.new_label()
        if self.false_label == '':
            self.false_label = self.generador.new_label()

    def end_commnet(self):
        self.generador.new_commnet('Fin acceso')
        self.generador.new_comment_line()
        self.generador.line_break()