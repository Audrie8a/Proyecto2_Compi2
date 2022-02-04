from Environment.Symbol import Symbol
from Expression.Primitive import Primitive
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Abstract.Instruction import Instruction
from Environment.Listas import Listas

class atributosStruct(Instruction):

    def __init__(self, id: str, type: typeExpression,linea, columna) -> None:
        self.id = id
        self. type = type
        self.value = None
        self.linea=linea
        self.columna=columna

    def setValue(self, value: Expression):
        self.value = value

    def execute(self, environment: Environment):
        print("")
        
    
        