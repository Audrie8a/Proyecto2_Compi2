from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas

class Equal(Expression):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right

    def compile(self, environment: Environment) -> Value:
        
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        if(leftValue.type == typeExpression.INTEGER or leftValue.type == typeExpression.FLOAT):

            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):

                newValue=Impresiones.imprimirRelatonals(self.generator,leftValue.getValue(),rightValue.getValue(),"IgualIgual")
                return Value(newValue,True,typeExpression.BOOL)
        elif (leftValue.type==typeExpression.STRING):
            if(rightValue.type==typeExpression.STRING):
                newValue=Impresiones.imprimirRelationalsStr(self.generator,leftValue.getValue(),rightValue.getValue(),"IgualIgualStr")
                return Value(newValue,True,typeExpression.BOOL)
        elif(leftValue.type == typeExpression.BOOL):

            if(rightValue.type == typeExpression.BOOL):
                izq="0"
                der="0"
                if leftValue.getValue()=="true":
                    izq="1"
                if rightValue.getValue()=="true":
                    der="1"
                newValue=Impresiones.imprimirRelatonals(self.generator,izq,der,"IgualIgual")
                return Value(newValue,True,typeExpression.BOOL)
        else:
            print("Error en IgualIgual")
            Listas.saveError("Error en IgualIgual",0,0)
            return Value("0",False,typeExpression.BOOL) 
                