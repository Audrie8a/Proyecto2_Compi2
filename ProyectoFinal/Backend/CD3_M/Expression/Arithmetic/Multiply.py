from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas

class Multiply(Expression):

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
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"*")
                return Value(newTemp,True,rightValue.type)
            else:
                print("Error en multiplicacion")
                Listas.saveError("Error en multiplicacion",0,0)
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.FLOAT):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"*")
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en multiplicacion")
                Listas.saveError("Error en multiplicacion",0,0)
                return Value("0",False,typeExpression.INTEGER)
        elif(leftValue.type==typeExpression.STRING):
            if(rightValue.type==typeExpression.STRING):
                cadena1=leftValue.value
                cadena2=rightValue.value
                cadena= cadena1+cadena2
                return Value(cadena,False,typeExpression.STRING)
            print("Error en multiplicacion, las cadenas sólo pueden multiplicarse entre sí!")
            Listas.saveError("Error en multiplicacion, las cadenas sólo pueden multiplicarse entre sí!",0,0)
            return Value("0",False,typeExpression.STRING)
        else:
                print("Error en multiplicacion")
                Listas.saveError("Error en multiplicacion",0,0)
                return Value("0",False,typeExpression.INTEGER)