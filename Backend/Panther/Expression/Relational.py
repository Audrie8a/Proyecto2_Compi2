from Enum.typeExpression import typeExpression
from Enum.relationalOperation import relationalOperation
from Enum.DominantRelatonal import DominantRelational
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Listas import Listas
class Relational(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: relationalOperation,linea, columna):
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
        #linea y columna
        line=self.linea
        column= self.columna
        #Obtenemos nuestro dominante
        dominant = DominantRelational[leftValue.getType().value][rightValue.getType().value]
        Error=""
        
        
        global izq  
        global der
        izq=True  
        der=True
        if(leftValue.getValue()=='false' or leftValue.getValue()=='False' or leftValue.getValue()==False and leftValue.getType()==3):
            izq=False
        if(rightValue.getValue()=='false' or rightValue.getValue()=='False' or rightValue.getValue()==False and rightValue.getType()==3):
            der=False

        try:
            if(self.operation == relationalOperation.MAYORQ):
                if(dominant == typeExpression.BOOL):  
                
                    return Symbol(
                        "",
                        
                        izq > der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) > der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq > float(rightValue.getValue()),
                            typeExpression.BOOL
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        False,
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) > float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] > str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )   
                elif(dominant == typeExpression.ERROR):
                    Error=("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue())) + " y " + str(rightValue.getValue())
                    print("\nNo es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue())) + " y " + str(rightValue.getValue())
                    Listas.saveError("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue())) + " y " + str(rightValue.getValue() ,line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER, "",line,column
                        )
            
            elif(self.operation == relationalOperation.MENORQ):
                if(dominant == typeExpression.BOOL):    
                    return Symbol(
                        "",
                        izq< der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) < der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq < float(rightValue.getValue()),
                            typeExpression.BOOL, "",line,column
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        False,
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) < float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] < str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.ERROR):
                    Error=("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()) ,line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER, "",line,column
                        )
            
            elif(self.operation == relationalOperation.MAYORIGUAL):
                if(dominant == typeExpression.BOOL):    
                    return Symbol(
                        "",
                        izq >= der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) >= der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq >= float(rightValue.getValue()),
                            typeExpression.BOOL, "",line,column
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                    False,
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    
                    return Symbol(
                        "",
                        float(leftValue.getValue()) >= float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] >= str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.ERROR):
                    Error=("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()) ,line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER, "",line,column
                        )
            
            elif(self.operation == relationalOperation.MENORIGUAL):
                if(dominant == typeExpression.BOOL):    
                    return Symbol(
                        "",
                        izq <= der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) <= der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq <= float(rightValue.getValue()),
                            typeExpression.BOOL, "",line,column
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        False,
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) <= float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] <= str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.ERROR):
                    Error=("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    print("\nNo es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                    Listas.saveError("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + str(leftValue.getValue()) + " y " + str(rightValue.getValue()),line,column)
                    return Symbol(
                                "",
                                0,
                                typeExpression.INTEGER, "",line,column
                        )
            
            elif(self.operation == relationalOperation.IGUALIGUAL):
                if(dominant == typeExpression.BOOL):    
                    return Symbol(
                        "",
                        izq == der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) == der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq == float(rightValue.getValue()),
                            typeExpression.BOOL
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        str(leftValue.getValue()) == str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] == str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) == float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.ERROR):
                    # En caso que venga STRING con cualquier otro tipo
                        #IZQ
                    
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and rightValue.getType().value==0: #Int o Float
                        return Symbol(
                        "",
                        float(leftValue.getValue()) == str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==3 and rightValue.getType().value==0: #Booleano
                        return Symbol(
                        "",
                        izq == str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )

                        #DER

                    elif rightValue.getType().value==1 or rightValue.getType().value==2 and leftValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) == float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif rightValue.getType().value==3 and leftValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) == der,
                        typeExpression.BOOL, "",line,column
                        )
                    
                    # En caso que venga CHAR con cualquier otro tipo
                        #IZQ


                    elif leftValue.getType().value==1 or leftValue.getType().value==2 and rightValue.getType().value==6: #Int o Float
                        return Symbol(
                        "",
                        float(leftValue.getValue()) == str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==3 and rightValue.getType().value==6: #Booleano
                        return Symbol(
                        "",
                        izq == str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )

                        #DER

                    elif rightValue.getType().value==1 or rightValue.getType().value==2 and leftValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] == float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif rightValue.getType().value==3 and leftValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] == der,
                        typeExpression.BOOL, "",line,column
                        )

                    #En caso venga string y char o viceversa
                    elif leftValue.getType().value==0 and rightValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) == str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==6 and rightValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] == str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
        
            elif(self.operation == relationalOperation.DIFERENTE):
                if(dominant == typeExpression.BOOL):    
                    return Symbol(
                        "",
                        izq != der,
                        typeExpression.BOOL, "",line,column
                        )            
                elif(dominant == typeExpression.INTEGER):
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                        return Symbol(
                            "",
                            float(leftValue.getValue()) != der,
                            typeExpression.BOOL, "",line,column
                            )
                    elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                        return Symbol(
                            "",
                            izq != float(rightValue.getValue()),
                            typeExpression.BOOL, "",line,column
                            )
                elif(dominant == typeExpression.STRING):
                    return Symbol(
                        "",
                        str(leftValue.getValue()) != str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.CHAR):
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0] != str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.FLOAT):
                    return Symbol(
                        "",
                        float(leftValue.getValue()) != float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                elif(dominant == typeExpression.ERROR):
                    # En caso que venga STRING con cualquier otro tipo
                        #IZQ
                    
                    if (leftValue.getType().value==1 or leftValue.getType().value==2) and rightValue.getType().value==0: #Int o Float
                        return Symbol(
                        "",
                        float(leftValue.getValue()) != str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==3 and rightValue.getType().value==0: #Booleano
                        return Symbol(
                        "",
                        izq != str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )

                        #DER

                    elif rightValue.getType().value==1 or rightValue.getType().value==2 and leftValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) != float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif rightValue.getType().value==3 and leftValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) != der,
                        typeExpression.BOOL, "",line,column
                        )
                    
                    # En caso que venga CHAR con cualquier otro tipo
                        #IZQ


                    elif leftValue.getType().value==1 or leftValue.getType().value==2 and rightValue.getType().value==6: #Int o Float
                        return Symbol(
                        "",
                        float(leftValue.getValue()) != str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==3 and rightValue.getType().value==6: #Booleano
                        return Symbol(
                        "",
                        izq != str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )

                        #DER

                    elif rightValue.getType().value==1 or rightValue.getType().value==2 and leftValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] != float(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
                    elif rightValue.getType().value==3 and leftValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] != der,
                        typeExpression.BOOL, "",line,column
                        )
                    
                    #En caso venga string con char o viceversa
                    elif leftValue.getType().value==0 and rightValue.getType().value==6:
                        return Symbol(
                        "",
                        str(leftValue.getValue()) != str(rightValue.getValue())[0],
                        typeExpression.BOOL, "",line,column
                        )
                    elif leftValue.getType().value==6 and rightValue.getType().value==0:
                        return Symbol(
                        "",
                        str(leftValue.getValue())[0] != str(rightValue.getValue()),
                        typeExpression.BOOL, "",line,column
                        )
        except:
            Listas.saveError(Error,line,column)                    
            return Symbol("",False,typeExpression.BOOL, "",line,column)
                    
