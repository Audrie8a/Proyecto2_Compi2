from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas


class NotF(Expression):

    def __init__(self, left: Expression) -> None:
        super().__init__()
        self.leftExpression = left

    def compile(self, environment: Environment) -> Value:
        
        self.leftExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)

        if(leftValue.type == typeExpression.BOOL):

            izq="0"
                
            if hasattr(leftValue,"isTemp"):
                if leftValue.isTemp:
                    izq=leftValue.getValue()
                    

            if leftValue.getValue()=="true" or leftValue.getValue()=="1":
                izq="1"
                

            newValue=Impresiones.imprimirRelatonals(self.generator,izq,"","NotF")
            return Value(newValue,True,typeExpression.BOOL)
        else:
            print("Error en Not")
            Listas.saveError("Error en Not",0,0)
            return Value("0",False,typeExpression.BOOL) 
                