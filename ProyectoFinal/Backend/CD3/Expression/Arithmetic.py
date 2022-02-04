from Enum.typeExpression import typeExpression
from Enum.arithmeticOperation import arithmeticOperation
from Enum.Dominant import Dominant
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Listas import Listas
class Arithmetic(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: arithmeticOperation, linea, columna):
        self.leftExp = leftExp
        self.rightExp = rightExp
        self.operation = operation
        self.linea= linea
        self.columna=columna

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        # Resolvemos la expresion que viene de lado derecho
        rightValue = self.rightExp.execute(environment)
        #linea columna
        line=self.linea
        column = self.columna
        #Obtenemos nuestro dominante
        dominant = Dominant[leftValue.getType().value][rightValue.getType().value]
        Error=""

        try:
            if(self.operation == arithmeticOperation.PLUS):
                if(dominant == typeExpression.STRING):
                    Error=("\nNo es posible sumar entre cadenas" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible sumar entre cadenas" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible sumar entre cadenas",line,column)
                    return Symbol(
                        "",
                        None,
                        typeExpression.STRING,"",line,column
                        )
                elif(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        int(leftValue.getValue()) + int(rightValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) + float(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                else:
                    Error=("\nNo es posible sumar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible sumar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible sumar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER,"",line,column
                        )
            
            elif(self.operation == arithmeticOperation.MINUS):
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        int(leftValue.getValue()) - int(rightValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) - float(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                elif(dominant == typeExpression.STRING):
                    Error=("\nNo es posible restar entre cadenas " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible restar entre cadenas " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible restar entre cadenas " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    
                    return Symbol(
                        "",
                        None,
                        typeExpression.STRING,"",line,column
                        )
                else:
                    Error=("\nNo es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER,"",line,column
                        )

            elif(self.operation == arithmeticOperation.MULTIPLY):             
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        int(leftValue.getValue()) * int(rightValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) * float(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                elif(dominant == typeExpression.STRING):
                    if leftValue.getType().value==0 and rightValue.getType().value==0:
                        return Symbol(
                                "",
                                str(leftValue.getValue())+str(rightValue.getValue()),
                                typeExpression.STRING,"",line,column
                            )
                    else:                    
                        Error=("\nNo es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue())+". Se necesita Castear")
                        print("\nNo es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue())+". Se necesita Castear")
                        Listas.saveError("No es posible imprimir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue())+". Se necesita Castear",line,column)
                    
                        return Symbol(
                                "",
                                None,
                                typeExpression.STRING,"",line,column
                        )
                else:
                    Error=("\nNo es posible multiplicar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible multiplicar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible multiplicar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER,"",line,column
                        )

            elif(self.operation == arithmeticOperation.DIV):
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        int(leftValue.getValue()) / int(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) / float(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        None,
                        typeExpression.STRING,"",line,column
                        )
                else:
                    Error=("\nNo es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                        "",
                        0,
                        typeExpression.INTEGER,"",line,column
                        )
            
            elif(self.operation == arithmeticOperation.POW):
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        pow(int(leftValue.getValue()), int(rightValue.getValue())),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        pow(float(leftValue.getValue()) , float(rightValue.getValue())),
                        typeExpression.FLOAT,"",line,column
                        )
                elif (dominant == typeExpression.STRING):
                    if leftValue.getType().value==0 and rightValue.getType().value==1:
                        return Symbol(
                                "",
                                str(leftValue.getValue())*rightValue.getValue(),
                                typeExpression.STRING,"",line,column
                        )
                    else:
                        Error=("\nNo es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()))
                        print("\nNo es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()))
                        Listas.saveError("No es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()),line,column)
                        return Symbol(
                                "",
                                None,
                                typeExpression.STRING,"",line,column
                        )
                else:
                    
                    Error=("\nNo es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()))
                    print("\nNo es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()))
                    Listas.saveError("No es posible elevar " +str( leftValue.getValue()) + " y " +str( rightValue.getValue()),line,column)
                    return Symbol(
                        "",
                        0,
                        typeExpression.INTEGER,"",line,column
                        )
            
            elif(self.operation == arithmeticOperation.MOD):
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        int(leftValue.getValue())% int(rightValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) %float(rightValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )            
                else:
                    Error=("\nNo es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible dividir " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                        "",
                        0,
                        typeExpression.INTEGER,"",line,column
                        )
            
            elif(self.operation == arithmeticOperation.UMENOS):
                if(dominant == typeExpression.INTEGER):
                    return Symbol(
                        "",
                        0-int(leftValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(0)-float(leftValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                        )
                elif(dominant == typeExpression.STRING):
                    Error=("\nNo es posible restar entre cadenas" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible restar entre cadenas" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible restar entre cadenas" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                        "",
                        None,
                        typeExpression.STRING,"",line,column
                        )
                else:
                    Error=("\nNo es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible restar " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                        "",
                        0,
                        typeExpression.INTEGER,"",line,column
                        )
        except:            
            Listas.saveError(Error,line,column)
            return Symbol('',0,typeExpression.INTEGER,"",line,column)