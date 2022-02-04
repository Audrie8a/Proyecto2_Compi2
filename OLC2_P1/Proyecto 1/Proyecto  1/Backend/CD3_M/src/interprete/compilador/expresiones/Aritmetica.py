from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.tipos.Tipo import (
    TipoArtimetico,
    TipoVar,
    get_tipo_var,
    verify_type,
)


class Aritmetica(Instruccion):
    def __init__(self, type, left, right, line, column):
        """
        Args:
            type (TipoAritmetico): Tipo de operacion
            left (Instruccion): operador izquierdo
            right (Instruccion): operador derecho
            line (number): linea
            column (number): columna
        """
        super().__init__(line, column)
        self.type = type
        self.left: Instruccion = left
        self.right: Instruccion = right
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        # self.generador.new_comment_line()
        # self.generador.new_commnet('inicio expresion aritmetica')
        left: Valor = self.left.compilar(entorno) if self.left else None
        right: Valor = self.right.compilar(entorno)

        if self.type == TipoArtimetico.POT:
            if (
                left.get_type() == TipoVar.STRING
                and right.get_type() == TipoVar.INT64
            ):
                return self.pot_str(left, right, entorno)
            return self.get_potencia(left, right)
        elif self.type == TipoArtimetico.POR:
            if (
                left.get_type() == TipoVar.STRING
                and right.get_type() == TipoVar.STRING
            ):
                return self.concat_string(left, right, entorno)
        elif self.type == TipoArtimetico.DIV:
            return self.compare_division(left, right, entorno)
        elif self.type == TipoArtimetico.MODULO:
            return self.mod_operation(left, right)

        left_value = left if left else Valor('0', TipoVar.INT64, False)

        if self.is_valid(left_value, right) is False:
            error_str = (
                'Op.izquierdor '
                + get_tipo_var(left_value.get_type())
                + ' no se puede operar con el Op.derecho '
                + get_tipo_var(right.get_type())
            )
            self.generador.new_error(error_str, self.line, self.column)
            print('error de tipos')
            return
        tipo_result = verify_type(left_value.get_type(), right.get_type())

        operation = self.get_type(self.type)
        temp = self.generador.new_temp()  # Nuevo Temporal -> t1...tn
        self.generador.new_exp(
            temp, left_value.get_value(), right.get_value(), operation
        )

        # self.generador.new_commnet('fin expresion aritmetica')
        # self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(temp, tipo_result, True)

    def get_type(self, operator: TipoArtimetico):
        if operator == TipoArtimetico.SUMA:
            return '+'
        elif (
            operator == TipoArtimetico.RESTA
            or operator == TipoArtimetico.UMENOS
        ):
            return '-'
        elif operator == TipoArtimetico.POR:
            return '*'
        elif operator == TipoArtimetico.DIV:
            return '/'
        elif operator == TipoArtimetico.POT:
            return '^'
        elif operator == TipoArtimetico.MODULO:
            return '%'
        else:
            return ''

    def get_potencia(self, left: Valor, right: Valor):
        # -------------- -> L0...Ln <- --------------
        while_lb = self.generador.new_label()  # L0: -> While Label
        exit_lb = self.generador.new_label()  # L1: -> Exit Label
        cero_lb = self.generador.new_label()
        # -------------- -> t0...tn <- --------------
        tmp_index = self.generador.new_temp()
        tmp_result = self.generador.new_temp()

        self.generador.new_exp(tmp_index, '0', '', '')  # t0 = 0
        self.generador.new_exp(tmp_result, '1', '', '')  # t1 = 1
        # -------------- -> L1 -> WHILE LABEL <- --------------
        if right.get_type() == TipoVar.FLOAT64:
            print('Error exponente es decimial')
            self.generador.new_error(
                'Expresion no es de tipo Int64', self.line, self.column
            )
            return
        tipo = verify_type(left.get_type(), right.get_type())
        if tipo == TipoVar.ERROR:
            error_str = (
                'El tipo "'
                + get_tipo_var(left.get_type())
                + '" y el tipo "'
                + get_tipo_var(right.get_type())
                + '" no se permite en la potencia'
            )
            self.generador.new_error(error_str, self.line, self.column)
            return
        self.generador.new_if(right.get_value(), '0', '==', cero_lb)
        self.generador.set_label(while_lb)  # L1:
        # if t0 == 2 { goto exit_label }
        self.generador.new_if(tmp_index, right.get_value(), '==', exit_lb)
        # t1 = 5 * t1
        self.generador.new_exp(tmp_result, left.get_value(), tmp_result, '*')
        # t0 = t0 + 1
        self.generador.new_exp(tmp_index, tmp_index, '1', '+')
        # goto while_label
        self.generador.new_goto(while_lb)

        # L3: -> Cero label
        self.generador.set_label(cero_lb)
        self.generador.new_exp(tmp_result, '1', '', '')

        self.generador.new_goto(exit_lb)

        self.generador.set_label(exit_lb)  # L1: -> exit label

        # self.generador.new_commnet('fin expresion aritmetica')
        # self.generador.new_comment_line()
        return Valor(tmp_result, tipo, True)

    def set_labels(self):
        pass

    def concat_string(self, left: Valor, right: Valor, entorno: Entorno):
        self.generador.concat_string()
        self.generador.new_comment_line()
        self.generador.new_commnet('paso de parametros')
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        # self.generador.free_temp(tmp_p)
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, left.get_value())
        # Guradar el segundo parametro
        self.generador.new_commnet('2do Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, right.get_value())
        self.generador.new_commnet('fin paso parametros')
        self.generador.new_comment_line()
        # Cambio de entorno para buscar los parametros
        self.generador.new_commnet('Cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('joinStr')
        # Guardar valor del return de la funcion
        self.generador.new_commnet('Guardar return de la funcion')
        return_p = self.generador.new_temp()
        # self.generador.free_temp(return_p)
        self.generador.get_stack(return_p, 'P')
        self.generador.new_commnet('Regreso entorno global')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        # self.generador.new_comment_line()
        self.generador.line_break()
        return Valor(return_p, TipoVar.STRING, True)

    def pot_str(self, left: Valor, right: Valor, entorno: Entorno):
        self.generador.pot_string()
        self.generador.new_comment_line()
        self.generador.new_commnet('Paso de parametros')
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        # self.generador.free_temp(tmp_p)
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, left.get_value())
        # Guardar segundo parametro
        self.generador.new_commnet('2do Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, right.get_value())
        self.generador.new_commnet('fin paso de parametros')
        self.generador.new_comment_line()
        # Cambio de parametro para buscar los parametros
        self.generador.new_commnet('cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('potenciaStr')
        # Gurdar el return de la funcion
        self.generador.new_commnet('Guardar el return de la funcion')
        return_p = self.generador.new_temp()
        # self.generador.free_temp(return_p)
        self.generador.get_stack(return_p, 'P')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        # self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(return_p, TipoVar.STRING, True)

    def compare_division(self, left: Valor, right: Valor, entorno: Entorno):
        self.generador.division_validate()
        self.generador.new_comment_line()
        self.generador.new_commnet('Paso de parametros')
        # Verificar tipos
        result_type = verify_type(left.get_type(), right.get_type())
        if result_type == TipoVar.ERROR:
            error_str = (
                'El tipo "'
                + get_tipo_var(left.get_type())
                + '" y el tipo "'
                + get_tipo_var(right.get_type())
                + '" no se permite en la division'
            )
            self.generador.new_error(error_str, self.line, self.column)
            return
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        # self.generador.free_temp(tmp_p)
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, left.get_value())
        # Guardar segundo parametro
        self.generador.new_commnet('2do Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, right.get_value())
        self.generador.new_commnet('fin paso de parametros')
        self.generador.new_comment_line()
        # Cambio de parametro para buscar los parametros
        self.generador.new_commnet('cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('divValidate')
        # Gurdar el return de la funcion
        self.generador.new_commnet('Guardar el return de la funcion')
        return_p = self.generador.new_temp()
        # self.generador.free_temp(return_p)
        self.generador.get_stack(return_p, 'P')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        # self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(return_p, TipoVar.FLOAT64, True)

    def is_valid(self, left: Valor, right: Valor):
        if (
            left.get_type() == TipoVar.INT64
            or left.get_type() == TipoVar.FLOAT64
        ):
            if (
                right.get_type() == TipoVar.INT64
                or right.get_type() == TipoVar.FLOAT64
            ):
                return True

        return False

    def mod_operation(self, left: Valor, right: Valor):
        result_type = verify_type(left.get_type(), right.get_type())
        if result_type == TipoVar.ERROR:
            error_str = (
                'El tipo "'
                + get_tipo_var(left.get_type())
                + '" y el tipo "'
                + get_tipo_var(right.get_type())
                + '" no se permite en el modulo'
            )
            self.generador.new_error(error_str, self.line, self.column)
            return

        temp = self.generador.new_temp()
        self.generador.mod_operation(temp, left.get_value(), right.get_value())
        return Valor(temp, result_type, True)