from src.interprete.compilador.tipos.Tipo import TipoVar


class SimboloArray:
    def __init__(self, tipo_array: TipoVar, subtipo: TipoVar):
        self.tipo_array = tipo_array
        self.subtipo = subtipo

    def get_subtipo(self):
        return self.subtipo

    def get_tipo_array(self):
        return self.tipo_array