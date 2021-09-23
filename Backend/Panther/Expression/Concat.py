from Enum.typeExpression import typeExpression
from Enum.concatOperation import concatOperation
from Enum.Dominant import Dominant
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Listas import Listas
class Concat(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: concatOperation, linea, columna):
        self.leftExp = leftExp
        self.rightExp = rightExp
        self.operation = operation
        self.linea=linea
        self.columna=columna

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        # Resolvemos la expresion que viene de lado derecho
        rightValue = self.rightExp.execute(environment)
        #linea columna
        line=self.linea
        column= self.columna
        dominant = Dominant[leftValue.getType().value][rightValue.getType().value]
        Error=""
        try:
            if(self.operation == concatOperation.COMMA):           
                    return Symbol(
                        "",
                        str(leftValue.getValue())+str(rightValue.getValue()),
                        typeExpression.STRING,"",line,column
            )
            
            elif(self.operation == concatOperation.UPPERCASE):
                if leftValue.getType().value==0:
                    return Symbol(
                            "",
                            str(leftValue.getValue()).upper(),
                            typeExpression.STRING,"",line,column
                        )
                else:                    
                    Error=("\nNo es posible imprimir " + str(leftValue.getValue()))
                    print("\nNo es posible imprimir " + str(leftValue.getValue()))
                    Listas.saveError("No es posible imprimir " + str(leftValue.getValue()),line,column)
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING,"",line,column
            )

            elif(self.operation == concatOperation.LOWERCASE):
                if leftValue.getType().value==0 :
                    return Symbol(
                            "",
                            str(leftValue.getValue()).lower(),
                            typeExpression.STRING,"",line,column
                        )
                else:                    
                    Error=("\nNo es posible imprimir " + str(leftValue.getValue()))
                    print("\nNo es posible imprimir " + str(leftValue.getValue()))
                    Listas.saveError("No es posible imprimir " + str(leftValue.getValue()),line,column)
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING,"",line,column
            )
            
            elif(self.operation == concatOperation.PARSE):
                return Symbol(
                            "",
                            str(leftValue.getValue()),
                            typeExpression.STRING,"",line,column
                        )

            else:
                Error=("No es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                print("No es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                Listas.saveError("No es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                return Symbol('',None,typeExpression.STRING,"",line,column)
        except:
            Listas.saveError(Error,line,column)
            return Symbol('',None,typeExpression.STRING,"",line,column)
