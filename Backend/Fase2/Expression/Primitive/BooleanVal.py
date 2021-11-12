from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Listas import Listas
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class BooleanVal(Expression):

    def __init__(self, type: typeExpression, value) -> None:
        super().__init__()
        self.type = type
        self.value = value

    def compile(self, environment: Environment) -> Value:
        
        if(self.type == typeExpression.BOOL ):
            if self.value=="true":
                self.value=1
            else:
                self.value=0
            return Value(str(self.value),False,self.type)

        print("No se reconoce el tipo")
        Listas.saveError("No se reconoce el tipo",0,0)
        return Value("0",False,typeExpression.INTEGER)