from src.interprete.compilador.tipos.Tipo import TipoVar
from src.interprete.compilador.simbolos.SimboloFuncion import SimboloFuncion
from src.interprete.compilador.simbolos.Entorno import Entorno
from src.interprete.compilador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, id, params_list, instruccions, line, column, tipo):
        super().__init__(line, column)
        self.id = id
        self.param_list: list = params_list
        self.instruccions: Instruccion = instruccions
        self.tipo = tipo
        self.line = line
        self.column = column
        self.pre_compie = True

    def compilar(self, entorno: Entorno):
        if self.pre_compie:
            self.pre_compie = False
            funct_simbol: SimboloFuncion = entorno.save_function(
                self.id, self.param_list, self.instruccions, self.tipo
            )
            if funct_simbol is None:
                self.generador.new_error(
                    f'Error, la funcion "{self.id}" ya existe', self.line, self.column
                )
                return

        new_env = Entorno(entorno)
        funct_simbol = entorno.get_function(self.id)
        return_lb = self.generador.new_label()

        # tmp_record = self.generador.get_temp_record()

        new_env.set_enviroment_funct(funct_simbol, return_lb)

        for param in self.param_list:
            new_var = new_env.save_variable(
                param.get_id(),
                param.get_type(),
                (
                    param.get_type() == TipoVar.STRING
                    or param.get_type() == TipoVar.STRUCT
                ),
            )
            if new_var is not None:
                if new_var.get_type() == TipoVar.STRUCT:
                    new_var.set_type_struct(param.get_type_aux())
                elif new_var.get_type() == TipoVar.ARRAY:
                    new_var.set_tipo_aux(param.get_type_aux_array())

        self.generador.free_all_temps()

        self.generador.new_begin_func(self.id)
        self.instruccions.compilar(new_env)

        if isinstance(self.tipo, TipoVar):
            if self.tipo != TipoVar.VOID:
                self.generador.set_label(return_lb)
        else:
            self.generador.set_label(return_lb)

        self.generador.new_end_funct()
        self.generador.free_all_temps()

    def set_labels(self):
        pass