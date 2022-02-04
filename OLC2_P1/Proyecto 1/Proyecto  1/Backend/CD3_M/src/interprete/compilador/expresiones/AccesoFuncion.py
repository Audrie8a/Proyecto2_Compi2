from src.interprete.compilador.simbolos.SimboloStruct import SimboloStruct
from src.interprete.compilador.tipos.Tipo import TipoVar, get_tipo_var
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.SimboloFuncion import SimboloFuncion
from src.interprete.compilador.abstracto.Instruccion import Instruccion
from src.interprete.compilador.simbolos.Entorno import Entorno


class AccesoFuncion(Instruccion):
    def __init__(self, id, param_values, line, column):
        super().__init__(line, column)
        self.id = id
        self.param_exp: list = param_values
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        funct_simbol: SimboloFuncion = entorno.search_function(self.id)
        if funct_simbol is not None:
            self.generador.line_break()
            self.generador.begin_comment(f'Llamado a funcion: {self.id}')
            params_values: list = []
            size = self.generador.save_temps(entorno)

            paramas_lenght_funct = funct_simbol.get_size_params()
            send_param_lenght = len(self.param_exp)

            if paramas_lenght_funct != send_param_lenght:
                self.generador.new_error(
                    f'Se esperaba {paramas_lenght_funct} argumentos, enviados {send_param_lenght}',
                    self.line,
                    self.column,
                )
                return

            i = 0
            for exp in self.param_exp:
                param_send: Valor = exp.compilar(entorno)
                param_registered = funct_simbol.get_value_param(i)
                if param_registered.get_type() == TipoVar.ARRAY:
                    pass
                elif param_send.get_type() != param_registered.get_type():
                    self.generate_error(
                        param_send.get_type(), param_registered.get_type()
                    )
                    return

                if param_send.get_type() == TipoVar.BOOLEAN:
                    tmp = self.generador.new_temp()
                    tmp_lb = self.generador.new_label()

                    self.generador.set_label(param_send.get_true_label())
                    self.generador.new_exp(
                        tmp, 'P', entorno.get_size() + i + 1, '+'
                    )
                    self.generador.set_stack(tmp, '1')
                    self.generador.new_goto(tmp_lb)

                    self.generador.set_label(param_send.get_false_label())
                    self.generador.new_exp(
                        tmp, 'P', entorno.get_size() + i + 1, '+'
                    )
                    self.generador.set_stack(tmp, '0')
                    self.generador.set_label(tmp_lb)

                params_values.append(param_send)
                i += 1

            tmp = self.generador.new_temp()

            if len(params_values) > 0:
                x = 0
                self.generador.new_exp(tmp, 'P', entorno.get_size() + 1, '+')
                for param in params_values:
                    if param.get_type() != TipoVar.BOOLEAN:
                        self.generador.set_stack(tmp, param.get_value())

                    if x != len(params_values) - 1:
                        self.generador.new_exp(tmp, tmp, '1', '+')

                    x += 1

            self.generador.new_entorno(entorno.get_size())
            self.generador.call_function(funct_simbol.get_id())
            self.generador.get_stack(tmp, 'P')
            self.generador.ret_entorno(entorno.get_size())
            self.generador.recover_tmp(entorno, size)

            if funct_simbol.get_type() != TipoVar.BOOLEAN:
                self.generador.end_comment('fin llamado a funcion')
                return Valor(tmp, funct_simbol.get_type(), True)

            aux_return = Valor("", funct_simbol.get_type(), False)
            self.set_labels()

            self.generador.new_if(tmp, '1', '==', self.true_label)
            self.generador.new_goto(self.false_label)

            aux_return.set_true_label(self.true_label)
            aux_return.set_false_label(self.false_label)
            self.generador.end_comment('fin llamado a funcion')
            return aux_return
        else:
            # ------------------------------------------------------------------
            # STRUCT
            # ------------------------------------------------------------------
            self.generador.line_break()
            self.generador.begin_comment(f'Declarar Struct {self.id}()')
            struct: SimboloStruct = entorno.get_struct(self.id)
            if struct is None:
                error_str = f'No existe "{self.id}"'
                self.generador.new_error(error_str, self.line, self.column)
                return
            if len(self.param_exp) != struct.get_size_att_list():
                error_str = (
                    'Se esperaban '
                    + struct.get_size_att_list()
                    + ' y se recibieron '
                    + len(self.param_exp)
                )
                self.generador.new_error(error_str, self.line, self.column)
                return

            self.struct_type = self.id

            tmp_saved = (
                self.generador.new_temp()
            )  # Apuntador se guarda el struct
            tmp_i_h = self.generador.new_temp()  # contador del heap

            self.generador.new_exp(tmp_saved, 'H', '', '')
            self.generador.new_exp(tmp_i_h, tmp_saved, '', '')

            # Almacenar el espacio del strcut
            self.generador.new_exp(
                'H',
                'H',
                struct.get_size_att_list(),
                '+',
                f'Almacenar espacio en heap del struct {self.id}',
            )

            i = 0
            for att in self.param_exp:
                att_send: Valor = att.compilar(entorno)
                att_registered = struct.get_attributo(i)
                if att_send.get_type() != att_registered.get_type():
                    erro_str = (
                        'Atributo de tipo '
                        + get_tipo_var(att_send.get_type())
                        + ' no se puede asiganar al atributo de tipo '
                        + get_tipo_var(att_registered.get_type())
                    )
                    self.generador.new_error(erro_str, self.line, self.column)
                    return

                if att_send.get_type() == TipoVar.BOOLEAN:
                    ret_lb = self.generador.new_label()
                    self.generador.set_label(att_send.get_true_label())
                    self.generador.set_heap(tmp_i_h, '1')
                    self.generador.new_goto(ret_lb)
                    self.generador.set_label(att_send.get_false_label())
                    self.generador.set_heap(tmp_i_h, '0')
                    self.generador.set_label(ret_lb)
                else:
                    self.generador.set_heap(tmp_i_h, att_send.get_value())

                self.generador.new_exp(tmp_i_h, tmp_i_h, '1', '+')
                i += 1

            return Valor(tmp_saved, TipoVar.STRUCT, True)

    def set_labels(self):
        if self.true_label == '':
            self.true_label = self.generador.new_label()
        if self.false_label == '':
            self.false_label = self.generador.new_label()

    def generate_error(self, tipo1: TipoVar, tipo2: TipoVar):
        erro_str = (
            'Argumento de tipo '
            + get_tipo_var(tipo1)
            + ' no se puede asiganar al parametro de tipo '
            + get_tipo_var(tipo2)
        )
        self.generador.new_error(erro_str, self.line, self.column)