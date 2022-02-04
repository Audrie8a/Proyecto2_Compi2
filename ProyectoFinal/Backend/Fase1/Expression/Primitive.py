
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression

class Primitive(Expression):

    def __init__(self, value, type: typeExpression,linea,columna):
        self.value = value
        self.type = type
        self.linea=linea
        self.columna=columna
    
    def execute(self, environment: Environment) -> Symbol:
        return Symbol("",self.value,self.type,"",self.linea,self.columna)