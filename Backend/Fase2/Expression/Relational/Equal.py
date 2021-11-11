from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones

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
                