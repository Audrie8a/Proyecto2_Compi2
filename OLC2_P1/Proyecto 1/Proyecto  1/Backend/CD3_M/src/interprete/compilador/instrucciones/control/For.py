from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class For(Instruccion):
    def __init__(self, id, exp_1, instructions, line, column, exp_2=None):
        super().__init__(line, column)
        self.id_var = id
        self.exp_1: Instruccion = exp_1
        self.exp_2: Instruccion = exp_2
        self.inst_list: Instruccion = instructions

    def compilar(self, entorno: Entorno):
        self.generador.begin_comment('Inicio For')
        new_env = Entorno(entorno)
        value_1: Valor = self.exp_1.compilar(entorno)
        if self.exp_2 is None:
            if value_1.get_type() == TipoVar.STRING:
                self.for_string(value_1, new_env)
            # elif value_1.get_type() == TipoVar.ARRAY:
            else:
                self.for_array(value_1, new_env)
        else:
            value_2: Valor = self.exp_2.compilar(entorno)
            self.for_normal(value_1, value_2, new_env)
        self.generador.end_comment('fin for')

    def set_labels(self):
        pass

    def for_normal(self, value_1: Valor, value_2: Valor, entorno: Entorno):

        if self.is_valid(value_1, value_2) is False:
            self.generador.new_error('Expresion no es de tipo Int64 or Float64')
            return

        new_var = entorno.save_variable(self.id_var, TipoVar.INT64, False)
        # -------------- -> ASIGNACION VARIABLE <- --------------
        tmp_pos = new_var.get_position()

        if not new_var.get_is_global():
            tmp_pos = self.generador.new_temp()
            self.generador.new_exp(tmp_pos, 'P', new_var.get_position(), '+')

        self.generador.set_stack(tmp_pos, value_1.get_value())
        self.generador.line_break()

        # -------------- -> FIN ASIGNACION VARIABLE <- --------------
        # -------------- -> L0...Ln <- --------------
        lb_while = self.generador.new_label()
        true_lb = self.generador.new_label()
        continue_lb = self.generador.new_label()  # continue label

        # -------------- -> WHILE <- --------------
        self.generador.set_label(lb_while)
        # Acceso a variable
        tmp_var = self.generador.new_temp()  # tmp para guardar var
        tmp_pos = new_var.get_position()  # Obtener posicion de la variable
        if not new_var.get_is_global():
            tmp_pos = self.generador.new_temp()
            self.generador.new_exp(
                tmp_pos,
                'P',
                new_var.get_position(),
                '+',
                'Posicionar el puntero',
            )
        self.generador.get_stack(tmp_var, tmp_pos)
        # if (t1 == 10) goto L1 -> Salir
        self.generador.new_if(tmp_var, value_2.get_value(), '>', true_lb)
        entorno.set_break(true_lb)
        entorno.set_continue(lb_while)
        self.inst_list.compilar(entorno)
        self.generador.new_goto(continue_lb)
        self.generador.line_break()
        self.generador.set_label(continue_lb)
        # Acceso a variable

        # Acceso a variable
        tmp_var = self.generador.new_temp()  # tmp para guardar var
        tmp_pos = new_var.get_position()  # Obtener posicion de la variable
        if not new_var.get_is_global():
            tmp_pos = self.generador.new_temp()
            self.generador.new_exp(
                tmp_pos,
                'P',
                new_var.get_position(),
                '+',
                'Posicionar el puntero',
            )
        self.generador.get_stack(tmp_var, tmp_pos)
        self.generador.new_exp(tmp_var, tmp_var, '1', '+')
        self.generador.set_stack(tmp_pos, tmp_var)

        self.generador.new_goto(lb_while)
        self.generador.set_label(true_lb)

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

    def for_array(self, value: Valor, entorno: Entorno):
        new_var = entorno.save_variable(
            self.id_var, value.get_aux_type(), False
        )
        # -------------- -> ASIGNACION VARIABLE <- --------------
        tmp_pos = new_var.get_position()
        if not new_var.get_is_global():
            tmp_pos = self.generador.new_temp()
            self.generador.new_exp(tmp_pos, 'P', new_var.get_position(), '+')

        # ------ CYCLE
        start = self.generador.new_label()
        label_true = self.generador.new_label()
        exit = self.generador.new_label()

        # pos_array: where start the array in heap
        pos_array = self.generador.new_temp()
        self.generador.new_exp(pos_array, value.get_value(), '', '')

        t0 = self.generador.new_temp()
        size = self.generador.new_temp()
        t1 = self.generador.new_temp()
        t2 = self.generador.new_temp()
        counter = self.generador.new_temp()
        value_array = self.generador.new_temp()
        index_array = self.generador.new_temp()

        self.generador.set_stack(tmp_pos, value.get_value())
        # getting size
        self.generador.get_stack(t0, tmp_pos)
        self.generador.get_heap(size, t0)

        # initializing the symbol value
        self.generador.new_exp(counter, '0', '', '')
        self.generador.new_exp(index_array, pos_array, '', '')
        self.generador.new_exp(index_array, index_array, '1', '+')

        self.generador.set_label(start)

        self.generador.new_exp(t2, 'P', tmp_pos, '+')
        self.generador.get_stack(t1, t2)
        self.generador.new_if(counter, size, '<', label_true)
        self.generador.new_goto(exit)

        self.generador.set_label(label_true)

        self.generador.get_heap(value_array, index_array)
        self.generador.set_stack(new_var.get_position(), value_array)
        entorno.set_break(exit)
        entorno.set_continue(start)
        self.inst_list.compilar(entorno)

        self.generador.new_exp(counter, counter, '1', '+')
        self.generador.new_exp(index_array, index_array, '1', '+')

        self.generador.new_goto(start)

        self.generador.set_label(exit)

    def for_string(self, value: Valor, entorno: Entorno):
        # save var and getting ID
        variable = entorno.save_variable(self.id_var, TipoVar.CHAR, False)

        # get position of variable
        temp_pos = variable.get_position()
        if not variable.get_is_global():
            temp_pos = self.generador.new_temp()
            self.generador.new_exp(temp_pos, 'P', variable.get_position(), '+')

        self.generador.set_stack(temp_pos, value.get_value())
        # ------ CYCLE
        start = self.generador.new_label()
        label_true = self.generador.new_label()
        exit = self.generador.new_label()

        value_string = self.generador.new_temp()
        index_string = self.generador.new_temp()

        # index_string: where start the array in heap
        self.generador.new_exp(index_string, value.get_value(), '', '')

        self.generador.set_label(start)
        # get variable and assign value
        self.generador.get_heap(value_string, index_string)

        self.generador.new_if(value_string, '- 1', '!=', label_true)
        self.generador.new_goto(exit)

        self.generador.set_label(label_true)
        self.generador.set_stack(variable.get_position(), value_string)

        entorno.set_break(exit)
        entorno.set_continue(start)
        self.inst_list.compilar(entorno)

        # ------ get and increase variables
        self.generador.new_exp(index_string, index_string, '1', '+')
        # ------ start again
        self.generador.new_goto(start)
        self.generador.set_label(exit)