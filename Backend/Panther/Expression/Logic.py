from Enum.typeExpression import typeExpression
from Enum.logicOperation import logicOperation
from Enum.Dominant import Dominant
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression

class Logic(Expression):

    def __init__(self, leftExp: Expression, rightExp: Expression, operation: logicOperation):
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
        
        global izq  
        global der
        izq=True  
        der=True
        if(leftValue.getValue()=='false' or leftValue.getValue()=='False' or leftValue.getValue()==False and leftValue.getType().value==3):
            izq=False
        if(rightValue.getValue()=='false' or rightValue.getValue()=='False' or rightValue.getValue()==False and rightValue.getType().value==3):
            der=False

        if(self.operation == logicOperation.AND):
            if(dominant == typeExpression.ERROR):
                print("No es posible operar tipos de datos diferentes a Bool" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(dominant == typeExpression.BOOL):
                return Symbol(
                    "",
                    izq and der,
                    typeExpression.BOOL
                    )            
        
        elif(self.operation == logicOperation.OR):
            if(dominant == typeExpression.ERROR):
                print("No es posible operar tipos de datos diferentes a Bool" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(dominant == typeExpression.BOOL):
                return Symbol(
                    "",
                    izq or der,
                    typeExpression.BOOL
                    )  
        
        elif(self.operation == logicOperation.NOT):
            if(dominant == typeExpression.ERROR):
                print("No es posible operar tipos de datos diferentes a Bool" + str(leftValue.getValue()) + " y " + str(rightValue.getValue()))
                return Symbol(
                    "",
                    None,
                    typeExpression.STRING
                    )
            elif(dominant == typeExpression.BOOL):
                return Symbol(
                    "",
                    not izq,
                    typeExpression.BOOL
                    )    