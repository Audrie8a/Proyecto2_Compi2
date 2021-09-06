from Enum.typeExpression import typeExpression
from Enum.concatOperation import concatOperation
from Enum.Dominant import Dominant
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression

class Concat(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: concatOperation):
        self.leftExp = leftExp
        self.rightExp = rightExp
        self.operation = operation

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        # Resolvemos la expresion que viene de lado derecho
        rightValue = self.rightExp.execute(environment)
        dominant = Dominant[leftValue.getType().value][rightValue.getType().value]
        
        try:
            if(self.operation == concatOperation.COMMA):           
                    return Symbol(
                        "",
                        str(leftValue.getValue())+str(rightValue.getValue()),
                        typeExpression.STRING
            )
            
            elif(self.operation == concatOperation.UPPERCASE):
                if leftValue.getType().value==0:
                    return Symbol(
                            "",
                            str(leftValue.getValue()).upper(),
                            typeExpression.STRING
                        )
                else:                    
                    print("\nNo es posible imprimir " + str(leftValue.getValue()))
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING
            )

            elif(self.operation == concatOperation.LOWERCASE):
                if leftValue.getType().value==0 :
                    return Symbol(
                            "",
                            str(leftValue.getValue()).lower(),
                            typeExpression.STRING
                        )
                else:                    
                    print("\nNo es posible imprimir " + str(leftValue.getValue()))
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING
            )
            
            elif(self.operation == concatOperation.PARSE):
                return Symbol(
                            "",
                            str(leftValue.getValue()),
                            typeExpression.STRING
                        )

            else:
                print("No es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol('',None,typeExpression.STRING)
        except:
            print("\n Error al obtener Cadena")
        return Symbol('',None,typeExpression.STRING)
