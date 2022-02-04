from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class If(Instruccion):
    def __init__(self, condition, instruccions, line, column, else_st=None):
        """IF
        Args:
            condition (Instruccino): condicion del if
            instruccions (list): lista de instrucciones
            line (int): linea
            column (column): columna
            else_st (instruccion, optional): Instruccion del else. Defaults to None.
        """
        super().__init__(line, column)
        self.condition: Instruccion = condition
        self.inst_list: Instruccion = instruccions
        self.else_st = else_st
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        self.generador.begin_comment('Inicio If')
        condition: Valor = self.condition.compilar(entorno)

        if condition.get_type() != TipoVar.BOOLEAN:
            self.generador.new_error(
                'Condicion no de tipo boolean', self.line, self.column
            )
            self.generador.end_comment('Fin If')
            return
        # Revisar que si crea un nuevo entorno
        # new_env = Entorno(entorno)
        self.generador.set_label(condition.get_true_label())
        # -------------- -> EJECUTAR INSTRUCCINOES <- --------------
        self.inst_list.compilar(entorno)
        # -------------- -> FIN DE EJECUCION  <- --------------

        if self.else_st is not None:
            end_lb = self.generador.new_label()
            self.generador.new_goto(end_lb)
            self.generador.set_label(condition.get_false_label())

            # -------------- -> EJECUTAR INSTRUCCIONES <- --------------
            # print(self.else_st)
            # for inst in self.else_st:
            #     inst.compilar(new_env)
            self.else_st.compilar(entorno)
            # -------------- -> FIN DE EJECUCION  <- --------------

            self.generador.set_label(end_lb)

        else:
            self.generador.set_label(condition.get_false_label())

        self.generador.end_comment('fin If')

    def set_labels(self):
        pass