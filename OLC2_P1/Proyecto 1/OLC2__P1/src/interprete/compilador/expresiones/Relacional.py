from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.tipos.Tipo import TipoRelational, TipoVar


class Relacional(Instruccion):
    def __init__(self, type, left, right, line, column):
        """
        Args:
            type (TipoRelacional): Tipo de operacion
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
        # self.generador.new_commnet('INICIO EXPRESION RELACIONAL')
        left: Valor = self.left.compilar(entorno)
        right = None
        value = Valor(None, TipoVar.BOOLEAN, False)

        if left.get_type() != TipoVar.BOOLEAN:
            right: Valor = self.right.compilar(entorno)
            if (
                left.get_type() == TipoVar.INT64
                or left.get_type() == TipoVar.FLOAT64
            ) and (
                right.get_type() == TipoVar.INT64
                or right.get_type() == TipoVar.FLOAT64
            ):

                # TRUE -> L0...Ln
                # FALSE -> L1..Ln
                self.set_labels()

                # -------------- -> IF <- --------------
                # if left op right { goto true_label; }
                # goto false_label;
                self.generador.new_if(
                    left.get_value(),
                    right.get_value(),
                    self.get_operation(self.type),
                    self.true_label,
                )
                self.generador.new_goto(self.false_label)  # goto false_lb
                value.set_true_label(self.true_label)
                value.set_false_label(self.false_label)
            elif (
                left.get_type() == TipoVar.STRING
                and right.get_type() == TipoVar.STRING
            ):
                if self.type != TipoRelational.COMPARACION:
                    self.generador.new_error(
                        'Solo se puedo comparar str', self.line, self.column
                    )
                    return

                self.set_labels()
                result: Valor = self.validate_str(left, right, entorno)
                # -------------- -> IF <- --------------
                # if left op right { goto true_label; }
                # goto false_label;
                self.generador.new_if(
                    result.get_value(), 1, '==', self.true_label
                )
                self.generador.new_goto(self.false_label)  # goto false_lb
                value.set_true_label(self.true_label)
                value.set_false_label(self.false_label)

        else:
            # ------------------------------------------------------------------
            # BOOLEAN
            # ------------------------------------------------------------------
            # -------------- -> L0...Ln <- --------------
            # PRIMITIVE LABEL, las pone el primitivo
            # goto L0;
            # goto L1;
            # L0:
            #   t0 = algo
            goto_right_lb = self.generador.new_label()
            temp_left = self.generador.new_temp()  # t0 = Null

            # -------------- -> LABEL TRUE <- --------------
            self.generador.set_label(left.get_true_label())  # L0:
            self.generador.new_exp(temp_left, '1', '', '')  # t0 = 1
            self.generador.new_goto(goto_right_lb)  # goto right_label
            # -------------- -> LABEL FALSE <- --------------
            self.generador.set_label(left.get_false_label())  # L1:
            self.generador.new_exp(temp_left, '0', '', '')  # t0 = 0

            # -------------- -> LABEL RIGHT <- --------------
            # L2 -> RIGHT LABEL:
            # PRIMITIVE LABEL, las pone primitivo
            # goto L3
            # goto l4

            self.generador.set_label(goto_right_lb)  # right_label:
            right: Valor = self.right.compilar(entorno)
            if right.get_type() != TipoVar.BOOLEAN:
                print('NO SE PUEDE COMPARAR')
                self.generador.new_error(
                    'Expresion no es de tipo boolean', self.line, self.column
                )
                return

            if_label = self.generador.new_label()  # etiqueta if o de escape
            right_temp = self.generador.new_temp()  # t1 = None

            # -------------- -> TRUE LABEL <- --------------
            self.generador.set_label(right.get_true_label())  # TRUE LABEL
            self.generador.new_exp(right_temp, '1', '', '')  # t1 = 1
            self.generador.new_goto(if_label)  #  goto if_label

            # -------------- -> FALSE LABEL <- --------------
            self.generador.set_label(right.get_false_label())  # L4: FALSE_LABEL
            self.generador.new_exp(right_temp, '0', '', '')  # t1 = 0

            # -------------- -> IF LABEL <- --------------
            # true_label = self.generador.new_label()
            # false_label = self.generador.new_label()
            self.set_labels()

            self.generador.set_label(if_label)  # L5:
            self.generador.new_if(
                temp_left,
                right_temp,
                self.get_operation(self.type),
                self.true_label,
            )  # if true == true { goto true_label; }

            self.generador.new_goto(self.false_label)  # goto { false_label; }
            value.set_true_label(self.true_label)
            value.set_false_label(self.false_label)

        # self.generador.new_commnet('FIN EXPRESION RELACIONAL')
        # self.generador.new_comment_line()
        return value

    def get_operation(self, operation: TipoRelational):
        if operation == TipoRelational.MAYORQ:
            return '>'
        elif operation == TipoRelational.MENORQ:
            return '<'
        elif operation == TipoRelational.MAYORI:
            return '>='
        elif operation == TipoRelational.MENORI:
            return '<='
        elif operation == TipoRelational.COMPARACION:
            return '=='
        elif operation == TipoRelational.DIFERENTE:
            return '!='
        return ''

    def set_labels(self):
        if self.true_label == '':
            self.true_label = self.generador.new_label()
        if self.false_label == '':
            self.false_label = self.generador.new_label()

    def validate_str(self, left: Valor, right: Valor, entorno: Entorno):
        self.generador.verify_equals_str()
        self.generador.line_break()
        self.generador.new_comment_line()
        # self.generador.new_commnet('Paso de parametros')
        # Temporal para almacenar parametros
        tmp_p = self.generador.new_temp()
        # self.generador.free_temp(tmp_p)
        self.generador.new_exp(tmp_p, 'P', entorno.get_size(), '+')
        # Guardar primer parametro
        # self.generador.new_commnet('1er Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, left.get_value())
        # Guardar segundo parametro
        # self.generador.new_commnet('2do Parametro')
        self.generador.new_exp(tmp_p, tmp_p, '1', '+')
        self.generador.set_stack(tmp_p, right.get_value())
        # self.generador.new_commnet('fin paso de parametros')
        # self.generador.new_comment_line()
        # Cambio de parametro para buscar los parametros
        # self.generador.new_commnet('cambio de entorno')
        self.generador.new_entorno(entorno.get_size())
        self.generador.call_function('isEqualsStr')
        # Gurdar el return de la funcion
        # self.generador.new_commnet('Guardar el return de la funcion')
        return_p = self.generador.new_temp()
        # self.generador.free_temp(return_p)
        self.generador.get_stack(return_p, 'P')
        self.generador.ret_entorno(entorno.get_size())

        # self.generador.new_commnet('fin expresion aritmetica')
        self.generador.new_comment_line()
        self.generador.line_break()

        return Valor(return_p, TipoVar.BOOLEAN, True)