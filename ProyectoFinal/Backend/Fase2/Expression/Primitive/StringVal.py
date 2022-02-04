from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas

class StringVal(Expression):

    def __init__(self, type: typeExpression, value) -> None:
        super().__init__()
        self.type = type
        self.value = value

    def compile(self, environment: Environment) -> Value:
        
        if(self.type == typeExpression.STRING):
            return Value(str(self.value),False,self.type)

        print("No se reconoce el tipo")
        Listas.saveError("No se reconoce el tipo",0,0)
        return Value("0",False,typeExpression.INTEGER)