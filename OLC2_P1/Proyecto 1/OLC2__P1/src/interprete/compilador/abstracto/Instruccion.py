from abc import ABC, abstractmethod
from src.interprete.compilador.simbolos.Generador import Generador

from src.interprete.compilador.simbolos.Entorno import Entorno


class Instruccion(ABC):
    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.true_label = ''
        self.false_label = ''
        self.struct_type = None
        self.generador = Generador.get_instance()

    @abstractmethod
    def compilar(self, entorno: Entorno):
        pass

    @abstractmethod
    def set_labels(self):
        pass