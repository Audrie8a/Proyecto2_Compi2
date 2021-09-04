from Enum.typeExpression import typeExpression
from Enum.relationalOperation import relationalOperation
from Enum.DominantRelatonal import DominantRelational
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression

class Relational(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: relationalOperation):
        self.leftExp = leftExp
        self.rightExp = rightExp
        self.operation = operation

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        # Resolvemos la expresion que viene de lado derecho
        rightValue = self.rightExp.execute(environment)
        #Obtenemos nuestro dominante
        dominant = DominantRelational[leftValue.getType().value][rightValue.getType().value]
        
        
        global izq  
        global der
        izq=True  
        der=True
        if(leftValue.getValue()=='false' or leftValue.getValue()=='False' or leftValue.getValue()==False and leftValue.getType()==3):
            izq=False
        if(rightValue.getValue()=='false' or rightValue.getValue()=='False' or rightValue.getValue()==False and rightValue.getType()==3):
            der=False

        if(self.operation == relationalOperation.MAYORQ):
            if(dominant == typeExpression.BOOL):  
            
                return Symbol(
                    "",
                    
                    izq > der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) > der,
                        typeExpression.BOOL
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
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                return Symbol(
                    "",
                    float(leftValue.getValue()) > float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                print("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + leftValue.getValue()) + " y " + rightValue.getValue()
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
           
        elif(self.operation == relationalOperation.MENORQ):
            if(dominant == typeExpression.BOOL):    
                return Symbol(
                    "",
                    izq< der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) < der,
                        typeExpression.BOOL
                        )
                elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                    return Symbol(
                        "",
                        izq < float(rightValue.getValue()),
                        typeExpression.BOOL
                        )
            elif(dominant == typeExpression.STRING):
                return Symbol(
                    "",
                    False,
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                return Symbol(
                    "",
                    float(leftValue.getValue()) < float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                print("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + leftValue.getValue() + " y " + rightValue.getValue())
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
           
        elif(self.operation == relationalOperation.MAYORIGUAL):
            if(dominant == typeExpression.BOOL):    
                return Symbol(
                    "",
                    izq >= der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) >= der,
                        typeExpression.BOOL
                        )
                elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                    return Symbol(
                        "",
                        izq >= float(rightValue.getValue()),
                        typeExpression.BOOL
                        )
            elif(dominant == typeExpression.STRING):
                return Symbol(
                    "",
                   False,
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                
                return Symbol(
                    "",
                    float(leftValue.getValue()) >= float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                print("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + leftValue.getValue() + " y " + rightValue.getValue())
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
           
        elif(self.operation == relationalOperation.MENORIGUAL):
            if(dominant == typeExpression.BOOL):    
                return Symbol(
                    "",
                    izq <= der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) <= der,
                        typeExpression.BOOL
                        )
                elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                    return Symbol(
                        "",
                        izq <= float(rightValue.getValue()),
                        typeExpression.BOOL
                        )
            elif(dominant == typeExpression.STRING):
                return Symbol(
                    "",
                    False,
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                return Symbol(
                    "",
                    float(leftValue.getValue()) <= float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                print("No es posible una expresión relacional de cadenas con otros tipos de datos:  " + leftValue.getValue() + " y " + rightValue.getValue())
                return Symbol(
                            "",
                            0,
                            typeExpression.INTEGER
                    )
        
        elif(self.operation == relationalOperation.IGUALIGUAL):
            if(dominant == typeExpression.BOOL):    
                return Symbol(
                    "",
                    izq == der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) == der,
                        typeExpression.BOOL
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
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                return Symbol(
                    "",
                    float(leftValue.getValue()) == float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                if leftValue.getType().value==1 or leftValue.getType().value==2:
                    return Symbol(
                    "",
                    float(leftValue.getValue()) == str(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif leftValue.getType().value==3:
                    return Symbol(
                    "",
                    izq == str(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif rightValue.getType().value==1 or rightValue.getType().value==2:
                    return Symbol(
                    "",
                    str(leftValue.getValue()) == float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif rightValue.getType().value==3:
                    return Symbol(
                    "",
                     str(leftValue.getValue()) == der,
                    typeExpression.BOOL
                    )

        elif(self.operation == relationalOperation.DIFERENTE):
            if(dominant == typeExpression.BOOL):    
                return Symbol(
                    "",
                    izq != der,
                    typeExpression.BOOL
                    )            
            elif(dominant == typeExpression.INTEGER):
                if (leftValue.getType().value==1 or leftValue.getType().value==2) and(rightValue.getType().value==3) :
                    return Symbol(
                        "",
                        float(leftValue.getValue()) != der,
                        typeExpression.BOOL
                        )
                elif (rightValue.getType().value==1 or rightValue.getType().value==2) and(leftValue.getType().value==3) :
                    return Symbol(
                        "",
                        izq != float(rightValue.getValue()),
                        typeExpression.BOOL
                        )
            elif(dominant == typeExpression.STRING):
                return Symbol(
                    "",
                    str(leftValue.getValue()) != str(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.FLOAT):
                return Symbol(
                    "",
                    float(leftValue.getValue()) != float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
            elif(dominant == typeExpression.ERROR):
                if leftValue.getType().value==1 or leftValue.getType().value==2:
                    return Symbol(
                    "",
                    float(leftValue.getValue()) != str(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif leftValue.getType().value==3:
                    return Symbol(
                    "",
                    izq != str(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif rightValue.getType().value==1 or rightValue.getType().value==2:
                    return Symbol(
                    "",
                    str(leftValue.getValue()) != float(rightValue.getValue()),
                    typeExpression.BOOL
                    )
                elif rightValue.getType().value==3:
                    return Symbol(
                    "",
                     str(leftValue.getValue()) != der,
                    typeExpression.BOOL
                    )
                     
