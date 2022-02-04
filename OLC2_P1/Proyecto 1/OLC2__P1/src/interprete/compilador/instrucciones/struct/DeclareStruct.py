from src.interprete.compilador.tipos.Tipo import TipoVar, get_tipo_var
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.SimboloStruct import SimboloStruct
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class DeclararStruct(Instruccion):
    def __init__(self, name_struct, att_values, line, column):
        super().__init__(line, column)
        self.name_struct = name_struct
        self.att_values: list = att_values
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        # Se coloco en acceso a funcion
        self.generador.line_break()
        self.generador.begin_comment(f'Declarar Struct {self.name_struct}()')
        struct: SimboloStruct = entorno.get_struct(self.name_struct)
        if struct is None:
            error_str = f'No existe el struct "{self.name_struct}"'
            self.generador.new_error(error_str, self.line, self.column)
            return
        if len(self.att_values) != struct.get_size_att_list():
            error_str = (
                'Se esperaban '
                + struct.get_size_att_list()
                + ' y se recibieron '
                + len(self.att_values)
            )
            self.generador.new_error(error_str, self.line, self.column)
            return

        self.struct_type = self.name_struct

        tmp_saved = self.generador.new_temp()  # Apuntador se guarda el struct
        tmp_i_h = self.generador.new_temp()  # contador del heap

        self.generador.new_exp(tmp_saved, 'H', '', '')
        self.generador.new_exp(tmp_i_h, tmp_saved, '', '')

        # Almacenar el espacio del strcut
        self.generador.new_exp(
            'H',
            'H',
            struct.get_size_att_list(),
            '+',
            f'Almacenar espacio en heap del struct {self.name_struct}',
        )

        i = 0
        for att in self.att_values:
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
        pass