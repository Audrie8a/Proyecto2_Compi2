from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Truncate(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(line, column)
        self.exp: Instruccion = expresion

    def compilar(self, entorno: Entorno):
        valor: Valor = self.exp.compilar(entorno)
        if valor.get_type() != TipoVar.FLOAT64:
            self.generador.new_error(
                'Se esperaba Float64', self.line, self.column
            )
            return

        return self.truncate_number(valor, entorno)

    def set_labels(self):
        pass

    def truncate_number(self, valor: Valor, entorno: Entorno):
        self.generador.trucate_num()
        self.generador.line_break()
        self.generador.new_comment_line()
        # self.generador.new_commnet('Paso de parametros')
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        # self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, valor.get_value())
        # Guardar segundo parametro
        # self.generador.new_commnet('2do Parametro')
        # self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        # self.generador.set_stack(tmp_p, index)
        # self.generador.new_commnet('fin paso de parametros')
        # self.generador.new_comment_line()
        # Cambio de parametro para buscar los parametros
        # self.generador.new_commnet('cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('truncNum')
        # Gurdar el return de la funcion
        # self.generador.new_commnet('Guardar el return de la funcion')
        return_p = self.generador.new_temp()
        self.generador.get_stack(return_p, 'P')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(return_p, TipoVar.INT64, True)