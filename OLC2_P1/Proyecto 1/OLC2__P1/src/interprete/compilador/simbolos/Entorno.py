from src.interprete.compilador.simbolos.SimboloStruct import SimboloStruct
from src.interprete.compilador.simbolos.SimboloFuncion import SimboloFuncion
from src.interprete.compilador.simbolos.Simbolo import Simbolo
from src.interprete.compilador.tipos.Tipo import TipoStruct, TipoVar


class Entorno:
    def __init__(self, previous_enviroment=None):
        self.previous: Entorno = previous_enviroment
        self.size = 0
        self.variables: dict = {}
        self.functions: dict = {}
        self.structs: dict = {}
        self.break_lb = None
        self.continue_lb = None
        self.return_lb = None
        self.actual_function: SimboloFuncion = None
        self.is_previous()

    def is_previous(self):
        self.size = self.previous.size if self.previous else 0
        self.break_lb = self.previous.break_lb if self.previous else None
        self.continue_lb = self.previous.continue_lb if self.previous else None
        self.return_lb = self.previous.return_lb if self.previous else None
        self.actual_function = (
            self.previous.actual_function if self.previous else None
        )

    def get_size(self):
        return self.size

    def set_size(self, size: int):
        self.size = size

    # --------------------------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------------------------

    def save_variable(self, id: str, type: TipoVar, in_heap: bool):
        """Guardar Variable
        Args:
            id (str): identificador del la variable
            type (TipoVar): tipo de variable
            in_heap (bool): esta en el heap
        Returns:
            Simbolo | None: Nuevo simbolo agregado
        """
        if id in self.variables.keys():
            var: Simbolo = self.variables[id]
            var.set_type(type)
            var.set_in_heap(in_heap)
            var.set_is_global(self.previous == None)
            return var

        new_var = Simbolo(id, type, self.size, self.previous == None, in_heap)
        self.size += 1
        self.variables[id] = new_var
        return new_var

    def get_variable(self, id: str):
        entorno = self
        while entorno != None:
            if id in entorno.variables.keys():
                var: Simbolo = entorno.variables[id]
                return var
            entorno = entorno.previous
        return None

    # --------------------------------------------------------------------------
    # GLOBAL
    # --------------------------------------------------------------------------
    def get_global(self):
        entorno = self
        while entorno.previous != None:
            entorno = entorno.previous
        return entorno

    # --------------------------------------------------------------------------
    # TRANFERENCIA
    # --------------------------------------------------------------------------
    def set_break(self, break_lb: str):
        self.break_lb = break_lb

    def set_continue(self, continue_lb: str):
        self.continue_lb = continue_lb

    def set_return(self, return_lb: str):
        self.return_lb = return_lb

    def get_break(self):
        return self.break_lb

    def get_continue(self):
        return self.continue_lb

    def get_return(self):
        return self.return_lb

    # --------------------------------------------------------------------------
    # FUNCIONES
    # --------------------------------------------------------------------------
    def save_function(self, id: str, param_list: list, instruccions, tipo):
        """
        Save Function
        Args:
            id (str): identificador
            param_list (list): lista de parametros
            instruccions (Instruccion): instrucines a ejecutar
        """
        if id in self.functions.keys():
            return None

        new_function = SimboloFuncion(id, param_list, instruccions, tipo)
        self.functions[id] = new_function
        return new_function

    def search_function(self, id: str):
        entorno = self
        while entorno is not None:
            if id in entorno.functions.keys():
                func: SimboloFuncion = entorno.functions[id]
                return func

            entorno = entorno.previous
        return None

    def get_function(self, id: str):
        return self.functions[id]

    def set_enviroment_funct(
        self, now_function: SimboloFuncion, return_lb: str
    ):
        self.size = 1
        self.actual_function = now_function
        self.return_lb = return_lb

    def get_now_function(self):
        return self.actual_function

    # --------------------------------------------------------------------------
    # STRUCT
    # --------------------------------------------------------------------------

    def save_struct(self, id, att_list: list, type_struct=TipoStruct.INMUTABLE):
        if id in self.structs.keys():
            return None
        struct: SimboloStruct = SimboloStruct(id, att_list, type_struct)
        self.structs[id] = struct
        return struct

    def get_struct(self, id):
        env = self
        while env != None:
            if id in env.structs.keys():
                struct: SimboloStruct = env.structs[id]
                return struct
            env = env.previous
        return None