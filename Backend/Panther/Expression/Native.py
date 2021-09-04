from Enum.typeExpression import typeExpression
from Enum.nativeOperation import nativeOperation
from Enum.Dominant import Dominant
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
import math

class Native(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: nativeOperation):
        self.leftExp = leftExp
        self.rightExp = rightExp
        self.operation = operation

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        # Resolvemos la expresion que viene de lado derecho
        rightValue = self.rightExp.execute(environment)
        #Obtenemos nuestro dominante
        dominant = Dominant[leftValue.getType().value][rightValue.getType().value]
        
        if(self.operation == nativeOperation.LOGD):
            if(leftValue.getType().value == 0): #String
                print("No es posible sacar logaritmo base 10 de una cadena" + str(leftValue.getValue()) )
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(leftValue.getType().value == 1 or leftValue.getType().value == 2 ): #Integer
                return Symbol(
                    "",
                    math.log10(float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            else:
                print("No es posible sacar logaritmo base 10 de " + str(leftValue.getValue()) )
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        elif(self.operation == nativeOperation.LOG):
            if(dominant == typeExpression.INTEGER or dominant == typeExpression.FLOAT ):
                return Symbol(
                    "",
                    math.log(float(rightValue.getValue()), float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            elif(dominant == typeExpression.STRING):
                print("No es posible sacar logaritmo entre cadenas: " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            else:
                print("No es posible sacar logaritmo de  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )

        
        elif (self.operation == nativeOperation.SIN):
            if(leftValue.getType().value == 0): #String
                print("No es posible sacar Seno de una cadena" + str(leftValue.getValue()) )
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(leftValue.getType().value == 1 or leftValue.getType().value == 2): #Integer
                return Symbol(
                    "",
                    math.sin(float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            else:
                print("No es posible sacar Seno de " + str(leftValue.getValue()) )
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        elif (self.operation == nativeOperation.COS):
            if(leftValue.getType().value == 0): #String
                print("No es posible sacar Coseno de una cadena" + str(leftValue.getValue()) )
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(leftValue.getType().value == 1 or leftValue.getType().value == 2): #Integer
                return Symbol(
                    "",
                    math.cos(float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            else:
                print("No es posible sacar Coseno de " + str(leftValue.getValue()) )
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        elif (self.operation == nativeOperation.TAN):
            if(leftValue.getType().value == 0): #String
                print("No es posible sacar Tangente de una cadena" + str(leftValue.getValue()) )
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(leftValue.getType().value == 1 or leftValue.getType().value == 2): #Integer
                return Symbol(
                    "",
                    math.tan(float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            else:
                print("No es posible sacar Tangente de " + str(leftValue.getValue()) )
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        elif (self.operation == nativeOperation.SQRT):
            if(leftValue.getType().value == 0): #String
                print("No es posible sacar Raiz de una cadena" + str(leftValue.getValue()) )
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(leftValue.getType().value == 1 or leftValue.getType().value == 2): #Integer
                return Symbol(
                    "",
                    math.sqrt(float(leftValue.getValue())),
                    typeExpression.FLOAT
                    )            
            else:
                print("No es posible sacar Raiz de " + str(leftValue.getValue()) )
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        else:
            return Symbol('',0,typeExpression.INTEGER)