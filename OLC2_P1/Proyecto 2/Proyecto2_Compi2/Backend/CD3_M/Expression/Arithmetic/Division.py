from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Listas import Listas
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones

class Division(Expression):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right

    def compile(self, environment: Environment) -> Value:

        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        newTemp = self.generator.newTemp()

        if(leftValue.type == typeExpression.INTEGER):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                Impresiones.DivisionCero(self,self.generator,newTemp,leftValue.getValue(),rightValue.getValue())                
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en division")
                Listas.saveError("Error en division",0,0)
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.FLOAT):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                Impresiones.DivisionCero(self,self.generator,newTemp,leftValue.getValue(),rightValue.getValue()) 
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en division")
                Listas.saveError("Error en division",0,0)
                return Value("0",False,typeExpression.INTEGER)
        
        else:
                print("Error en division")
                Listas.saveError("Error en division",0,0)
                return Value("0",False,typeExpression.INTEGER)