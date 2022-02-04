from src.interprete.compilador.simbolos.Parametro import Parametro
from src.interprete.compilador.abstracto.Valor import Valor
from src.interprete.compilador.simbolos.Simbolo import Simbolo
from src.interprete.compilador.simbolos.SimboloStruct import SimboloStruct
from src.interprete.compilador.tipos.Tipo import (
    TipoStruct,
    TipoVar,
    get_tipo_var,
)
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class AsignarAccesoStruct(Instruccion):
    def __init__(self, id, att_list, exppresion, line, column):
        super().__init__(line, column)
        self.id = id
        self.att_list: list = att_list
        self.expresion: Instruccion = exppresion
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        variable: Simbolo = entorno.get_variable(self.id)
        if variable is None:
            self.generador.new_error(
                f'No existe la variable "{self.id}"', self.line, self.column
            )
            return
        if (
            variable.get_type() != TipoVar.STRUCT
            or variable.get_tyep_struct() is None
        ):
            self.generador.new_error(
                f'La variable "{self.id}" no es de tipo Struct',
                self.line,
                self.column,
            )
            return

        val_compiled: Valor = self.expresion.compilar(entorno)

        # -------------- -> T0...Tn <- --------------
        tmp_i = self.generador.new_temp()
        tmp_pos = variable.get_position()
        # -------------- -> Aux <- --------------
        i = 0
        att_type = None
        struct: SimboloStruct = entorno.get_struct(variable.get_tyep_struct())
        if not variable.get_is_global():
            tmp_pos = self.generador.new_temp()
            self.generador.new_exp(tmp_pos, 'P', variable.get_position(), '+')

        self.generador.get_stack(tmp_i, tmp_pos)

        for x in range(len(self.att_list)):
            if not self.is_mutable(struct):
                return
            att_search = self.att_list[x]
            att_type, i = self.search_att(att_search, struct)
            tmp_aux = tmp_i
            if att_type is None:
                self.generador.new_error(
                    f'El atributo "{att_search}" no es existe',
                    self.line,
                    self.column,
                )
                return
            if att_type.get_type() == TipoVar.STRUCT:
                struct2: SimboloStruct = entorno.get_struct(
                    att_type.get_type_aux()
                )
                if struct2 is None:
                    error_str = (
                        'No existe el Struct "' + att_type.get_type_aux() + '"'
                    )
                    self.generador.new_error(
                        error_str,
                        self.line,
                        self.column,
                    )
                    return
                struct = struct2

            if x == 0:
                self.generador.new_exp(tmp_aux, tmp_aux, i, '+')
                continue
            tmp_i = self.generador.new_temp()
            self.generador.get_heap(tmp_i, tmp_aux)
            self.generador.new_exp(tmp_i, tmp_i, i, '+')

        if val_compiled.get_type() == att_type.get_type():
            self.generador.set_heap(tmp_i, val_compiled.get_value())
        else:
            erro_str = (
                'Valor de tipo '
                + get_tipo_var(val_compiled.get_type())
                + ' no se puede asiganar al atributo de tipo '
                + get_tipo_var(att_type.get_type())
            )
            self.generador.new_error(erro_str, self.line, self.column)
            return

    def set_labels(self):
        pass

    def search_att(self, att_name, struct: SimboloStruct):
        i = 0
        for att in struct.get_att_list():
            att: Parametro
            if att.get_id() == att_name:
                att_type = att
                return att_type, i
            i += 1
        return None, None

    def is_mutable(self, struct: SimboloStruct):
        if struct.get_type_strcut() == TipoStruct.INMUTABLE:
            erro_str = 'Struct "' + struct.get_id() + '" es de tipo Inmutable'
            self.generador.new_error(erro_str, self.line, self.column)
            return False
        return True