from src.interprete.compilador.tipos.Tipo import TipoVar


class Valor:
    def __init__(self, value, type, is_temp: bool, aux_type: TipoVar = None):
        """
        Args:
            value (anay): valor
            type (any): tipo del valor
            is_temp (bool): es temporal
            aux_type (any, optional): Defaults to None.
        """
        self.value = value
        self.type = type
        self.is_temp = is_temp
        self.aux_type = aux_type
        self.true_label = ''
        self.false_label = ''
        self.aux_values_list = []
        self.aux_tyes_list = []

    # ==========================================================================
    # VALUE
    # ==========================================================================
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    # ==========================================================================
    # TIPO
    # ==========================================================================
    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    # ==========================================================================
    # IS_TEMP
    # ==========================================================================
    def set_is_temp(self, is_temp: bool):
        self.is_temp = is_temp

    def get_is_temp(self):
        return self.is_temp

    # ==========================================================================
    # AUX TYPE
    # ==========================================================================
    def set_aux_type(self, aux_type):
        self.aux_type = aux_type

    def get_aux_type(self):
        return self.aux_type

    def set_aux_types_list(self, aux_types: list):
        self.aux_types_list = aux_types

    def get_aux_types_list(self):
        return self.aux_types_list

    def set_aux_values_list(self, aux_values: list):
        self.aux_values_list = aux_values

    def get_aux_values_list(self):
        return self.aux_values_list

    # ==========================================================================
    # TRUE LABEL
    # ==========================================================================
    def set_true_label(self, label):
        self.true_label = label

    def get_true_label(self):
        return self.true_label

    # ==========================================================================
    # FALSE LABEL
    # ==========================================================================
    def set_false_label(self, label):
        self.false_label = label

    def get_false_label(self):
        return self.false_label