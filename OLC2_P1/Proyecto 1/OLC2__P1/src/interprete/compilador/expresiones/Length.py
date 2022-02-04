from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Length(Instruccion):
    def __init__(self, expresion, line, column):
        super().__init__(line, column)
        self.exp: Instruccion = expresion
        self.line = line
        self.column = line

    def compilar(self, entorno: Entorno):
        valor: Valor = self.exp.compilar(entorno)

        if valor.get_type() == TipoVar.STRING:
            return self.len_string(valor, entorno)
        else:
            if valor.get_type() == TipoVar.ARRAY:
                return self.len_array(valor)
            else:
                return self.len_array2(valor)
            # print(valor.get_type())
        # if (valor.get_type() == TipoVar.ARRAY) or (
        #     valor.get_type() == TipoVar.STRING
        # ):
        # else:
        #     self.generador.new_error(
        #         'Length solo esta disponible para Array o String',
        #         self.line,
        #         self.column,
        #     )
        #     return

    def set_labels(self):
        pass

    def len_array2(self, valor: Valor):
        tmp_saved = valor.get_value()
        self.generador.get_heap(tmp_saved, tmp_saved)
        return Valor(tmp_saved, TipoVar.INT64, True)

    def len_array(self, array: Valor):
        tmp_h_i = self.generador.new_temp()
        tmp_saved = self.generador.new_temp()

        self.generador.line_break()
        self.generador.begin_comment('Len array')
        self.generador.get_stack(tmp_h_i, array.get_value())
        self.generador.get_heap(tmp_saved, tmp_h_i)
        self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(tmp_saved, TipoVar.INT64, True)

    def len_string(self, string: Valor, entorno: Entorno):
        self.generador.get_len_str()
        self.generador.line_break()
        self.generador.new_comment_line()
        # self.generador.new_commnet('Paso de parametros')
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        # self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, string.get_value())
        # Guardar segundo parametro
        # self.generador.new_commnet('2do Parametro')
        # self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        # self.generador.set_stack(tmp_p, index)
        # self.generador.new_commnet('fin paso de parametros')
        # self.generador.new_comment_line()
        # Cambio de parametro para buscar los parametros
        # self.generador.new_commnet('cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('getLenStr')
        # Gurdar el return de la funcion
        # self.generador.new_commnet('Guardar el return de la funcion')
        return_p = self.generador.new_temp()
        self.generador.get_stack(return_p, 'P')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(return_p, TipoVar.INT64, True)