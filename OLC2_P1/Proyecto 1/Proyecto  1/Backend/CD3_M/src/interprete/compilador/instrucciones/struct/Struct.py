from src.interprete.compilador.tipos.Tipo import TipoStruct
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Struct(Instruccion):
    def __init__(self, id, att_list, line, column, type=TipoStruct.INMUTABLE):
        super().__init__(line, column)
        self.id = id
        self.att_list = att_list
        self.type = type
        self.line = line
        self.column = column

    def compilar(self, entorno: Entorno):
        struct_simbol = entorno.save_struct(self.id, self.att_list, self.type)
        if struct_simbol is None:
            error_str = f'El struct f"{self.id}" ya existe'
            self.generador.new_error(error_str, self.line, self.column)
            return

    def set_labels(self):
        pass