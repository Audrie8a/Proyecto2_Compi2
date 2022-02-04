from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.tipos.Tipo import TipoLogico, TipoVar
from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.simbolos.Entorno import Entorno


class Logica(Instruccion):
    def __init__(self, type, left, right, line, column):
        """
        Args:
            type (TipoLogico): Tipo de operacion
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
        # self.generador.new_commnet('INICIO EXPRESION LOGICA')

        self.set_labels()
        and_or_lb = ''

        if self.type == TipoLogico.AND:
            and_or_lb = self.left.true_label = self.generador.new_label()
            self.right.true_label = self.true_label
            self.left.false_label = self.right.false_label = self.false_label

        elif self.type == TipoLogico.OR:
            self.left.true_label = self.right.true_label = self.true_label
            and_or_lb = self.left.false_label = self.generador.new_label()
            self.right.false_label = self.false_label
        else:
            # ------------------------------------------------------------------
            # NOT !
            # ------------------------------------------------------------------
            # solo derecha
            self.right.true_label = self.false_label
            self.right.false_label = self.true_label

            self.right.compilar(entorno)

            value_ret = Valor(None, TipoVar.BOOLEAN, False)
            value_ret.set_true_label(self.true_label)
            value_ret.set_false_label(self.false_label)

            # self.generador.new_commnet('FIN EXPRESION LOGICA')
            # self.generador.new_comment_line()

            return value_ret

        left: Valor = self.left.compilar(entorno)
        if left.get_type() != TipoVar.BOOLEAN:
            print('No es una expresion booleana')
            self.generador.new_error(
                'No es una expresion booleana', self.line, self.column
            )
            return

        self.generador.set_label(and_or_lb)
        right: Valor = self.right.compilar(entorno)
        if right.get_type() != TipoVar.BOOLEAN:
            print('No es una expresion booleana')
            self.generador.new_error(
                'No es una expresion booleana', self.line, self.column
            )
            return

        # self.generador.new_commnet('FIN EXPRESION LOGICA')
        # self.generador.new_comment_line()
        valor = Valor(None, TipoVar.BOOLEAN, False)
        valor.set_true_label(self.true_label)
        valor.set_false_label(self.false_label)
        return valor

    def set_labels(self):
        if self.true_label == '':
            self.true_label = self.generador.new_label()
        if self.false_label == '':
            self.false_label = self.generador.new_label()