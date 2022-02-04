from src.interprete.compilador.tipos.Tipo import TipoVar


class Simbolo:
    def __init__(
        self,
        id: str,
        type: TipoVar,
        position: int,
        is_global: bool,
        in_heap: bool = False,
    ):
        """Constructor
        Args:
            id (str): id de la variable
            type (TipoVar): tipo de variable
            position (int): posicion
            is_global (bool): si es global o no
            in_heap (bool, optional): pertenece al heap. Defaults to False.
        """
        self.id = id
        self.type = type
        self.is_global: bool = is_global
        self.in_heap: bool = in_heap
        self.position: int = position
        self.value = None
        self.list_aux_types: list = []
        self.list_aux_values: list = []
        self.tipo_aux = None
        self.type_struct = None

    # ==========================================================================
    # SET AND GET: ID
    # ==========================================================================
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    # ==========================================================================
    # SET AND GET: TYPE
    # ==========================================================================
    def set_type(self, type: TipoVar):
        self.type = type

    def get_type(self):
        return self.type

    # ==========================================================================
    # SET AND GET: GLOBA_VAR
    # ==========================================================================
    def set_is_global(self, global_var: bool):
        self.is_global = global_var

    def get_is_global(self):
        return self.is_global

    # ==========================================================================
    # SET AND GET: IN_HEAP
    # ==========================================================================
    def set_in_heap(self, in_heap: bool):
        self.in_heap = in_heap

    def get_in_heap(self):
        return self.in_heap

    # ==========================================================================
    # SET AND GET: POSITION
    # ==========================================================================
    def set_position(self, position: int):
        self.position = position

    def get_position(self):
        return self.position

    # ==========================================================================
    # VALUE
    # ==========================================================================
    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_list_aux_types(self, list_types: list):
        self.list_aux_types = list_types

    def get_list_aux_types(self):
        return self.list_aux_types

    def set_list_aux_values(self, list_values: list):
        self.list_aux_values = list_values

    def get_list_aux_values(self):
        return self.list_aux_values

    def set_tipo_aux(self, tipo: TipoVar):
        self.tipo_aux = tipo

    def get_tipo_aux(self):
        return self.tipo_aux

    def set_type_struct(self, type_struct):
        self.type_struct = type_struct

    def get_tyep_struct(self):
        return self.type_struct