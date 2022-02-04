from src.interprete.compilador.simbolos.Parametro import Parametro
from src.interprete.compilador.tipos.Tipo import TipoVar


class SimboloFuncion:
    def __init__(self, id: str, param_list: list, instruccions, tipo: TipoVar):
        """Simbolo Funcion
        Args:
            id (str): identificador
            param_list (list): lista de parametros
            instruccions (Instruccion): instrucines a ejecutar
        """
        self.id = id
        self.param_list: list = param_list
        self.instruccions = instruccions
        self.tipo: TipoVar = tipo
        self.size_param = len(param_list)
        self.type_struct: str = None
        self.verify_type(tipo)

    def set_id(self, id: str):
        self.id = id

    def get_id(self):
        return self.id

    def set_param_list(self, param_list: list):
        self.param_list = param_list

    def get_param_list(self):
        return self.param_list

    def set_instruccions(self, instruccions):
        self.instruccions = instruccions

    def get_instruccions(self):
        return self.instruccions

    def get_size_params(self):
        return self.size_param

    def get_type(self):
        return self.tipo

    def set_type(self, type: TipoVar):
        self.tipo = type

    def get_value_param(self, index: int):
        param: Parametro = self.param_list[index]
        return param

    def verify_type(self, type):
        if isinstance(type, TipoVar):
            self.tipo = type
        else:
            self.type_struct = type
            self.tipo = TipoVar.STRUCT