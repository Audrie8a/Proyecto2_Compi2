from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas


class AndF(Expression):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right

    def compile(self, environment: Environment) -> Value:
        
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        if(leftValue.type == typeExpression.BOOL):

            if(rightValue.type == typeExpression.BOOL):
                izq="0"
                der="0"
                if hasattr(rightValue,"isTemp"):
                    if rightValue.isTemp:
                        der=rightValue.getValue()
                elif hasattr(leftValue,"isTemp"):
                    if leftValue.isTemp:
                        izq=leftValue.getValue()
                    

                if leftValue.getValue()=="true" or leftValue.getValue()=="1":
                    izq="1"
                if rightValue.getValue()=="true" or rightValue.getValue()=="1":
                    der="1"

                newValue=Impresiones.imprimirRelatonals(self.generator,izq,der,"AndF")
                return Value(newValue,True,typeExpression.BOOL)
        else:
            print("Error en And")
            Listas.saveError("Error en And",0,0)
            return Value("0",False,typeExpression.BOOL) 
                