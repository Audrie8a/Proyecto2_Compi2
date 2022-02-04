from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.tipos.Tipo import TipoVar


class Primitivo(Instruccion):
    def __init__(self, valor, type, line, column):
        """
        Args:
            value (any): valor del primitivo
            type (Tipo): tipo del primitvo
            line (number):
            column (number):
        """
        super().__init__(line, column)
        self.value = valor
        self.type = type

    def compilar(self, entorno: Entorno):
        self.generador.new_commnet(f'primitivo: {self.value}')
        valor_return = None
        if self.type == TipoVar.INT64 or self.type == TipoVar.FLOAT64:
            valor_return = Valor(self.value, self.type, False)
        elif self.type == TipoVar.BOOLEAN:
            self.set_labels()

            if self.value:
                self.generador.new_goto(self.true_label)  # goto L0
                text = 'False Label: evita error en go:' + self.false_label
                self.generador.new_commnet(text)
                self.generador.new_goto(self.false_label)  # goto L1, evita err
            else:
                self.generador.new_goto(self.false_label)  # goto L1
                text = 'true Label: evita error en go:' + self.true_label
                self.generador.new_commnet(text)
                self.generador.new_goto(self.true_label)  # goto L0, evita error

            valor_return = Valor(self.value, self.type, False)
            valor_return.set_true_label(self.true_label)
            valor_return.set_false_label(self.false_label)
            # return valor_return
        elif self.type == TipoVar.STRING:
            tmp_h = self.generador.new_temp()
            self.generador.line_break()
            self.generador.new_exp(tmp_h, 'H', '', '')

            for caracter in str(self.value):
                self.generador.set_heap('H', ord(caracter), caracter)
                self.generador.nex_heap()

            # Fin de cadena
            self.generador.set_heap('H', '-1', 'FIN CADENA')
            self.generador.nex_heap()

            self.generador.line_break()

            valor_return = Valor(tmp_h, TipoVar.STRING, True)
        else:
            valor_return = Valor(self.value, self.type, False)

        # self.generador.new_commnet('fin primitivo')
        # self.generador.new_comment_line()
        # self.generador.line_break()
        return valor_return

    def set_labels(self):
        if self.true_label == '':
            self.true_label = self.generador.new_label()  # L0...Ln
        if self.false_label == '':
            self.false_label = self.generador.new_label()  # L1...Ln