from src.interprete.compilador.simbolos.Parametro import Parametro
from src.interprete.compilador.tipos.Tipo import TipoStruct


class SimboloStruct:
    def __init__(
        self,
        id: str,
        att_list: list,
        type_struct: TipoStruct = TipoStruct.INMUTABLE,
    ):
        self.id = id
        self.att_list: list = att_list
        self.size_att = len(att_list)
        self.tipo_struct = type_struct

    def set_id(self, id: str):
        self.id = id

    def get_id(self):
        return self.id

    def set_att_list(self, att_list: list):
        self.att_list = att_list

    def get_att_list(self):
        return self.att_list

    def get_type_strcut(self):
        return self.tipo_struct

    def set_type(self, type: TipoStruct):
        self.tipo_struct = type

    def get_attributo(self, index: int):
        attributo: Parametro = self.att_list[index]
        return attributo

    def get_size_att_list(self):
        return self.size_att