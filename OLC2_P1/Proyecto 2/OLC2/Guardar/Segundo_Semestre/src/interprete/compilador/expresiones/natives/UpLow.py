from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.tipos.Tipo import TipoUpLowCase, TipoVar


class ToUpLowCase(Instruccion):
    def __init__(self, type, to_conv, line, column):
        super().__init__(line, column)
        self.type = type
        self.to_conv: Instruccion = to_conv
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        value: Valor = self.to_conv.compilar(entorno)
        if value.get_type() != TipoVar.STRING:
            self.generador.new_error(
                f'{value.get_value()}, no es de tipo string',
                self.line,
                self.column,
            )
            return
        if self.type == TipoUpLowCase.UPPER:
            return self.to_upper(value, entorno)
        else:
            return self.to_lower(value, entorno)

    def set_labels(self):
        pass

    def to_upper(self, value: Valor, entorno: Entorno):
        self.generador.to_upper()
        self.generador.line_break()
        temp_p = self.generador.new_temp()
        self.generador.new_exp(temp_p, 'P', entorno.get_size(), '+')
        # Guardar el primer parametro
        self.generador.new_exp(temp_p, temp_p, '1', '+')
        self.generador.set_stack(temp_p, value.get_value())
        # Cambio de entoro para buscar los parametros
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('toUpperCase')
        # Guardar el return de la funcion
        return_param = self.generador.new_temp()
        self.generador.get_stack(return_param, 'P')
        self.generador.ret_entorno(entorno.get_size())

        self.generador.line_break()

        return Valor(return_param, TipoVar.STRING, True)

    def to_lower(self, value: Valor, entorno: Entorno):
        self.generador.to_lower()
        self.generador.line_break()
        temp_p = self.generador.new_temp()
        self.generador.new_exp(temp_p, 'P', entorno.get_size(), '+')
        # Guardar el primer parametro
        self.generador.new_exp(temp_p, temp_p, '1', '+')
        self.generador.set_stack(temp_p, value.get_value())
        # Cambio de entoro para buscar los parametros
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('toLowerCase')
        # Guardar el return de la funcion
        return_param = self.generador.new_temp()
        self.generador.get_stack(return_param, 'P')
        self.generador.ret_entorno(entorno.get_size())

        self.generador.line_break()

        return Valor(return_param, TipoVar.STRING, True)