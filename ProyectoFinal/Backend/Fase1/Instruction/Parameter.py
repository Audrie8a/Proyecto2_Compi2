from Environment.Symbol import Symbol
from Expression.Primitive import Primitive
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Abstract.Instruction import Instruction
from Environment.Listas import Listas

class Parameter(Instruction):

    def __init__(self, id: str, type: typeExpression,linea, columna) -> None:
        self.id = id
        self. type = type
        self.value = None
        self.linea=linea
        self.columna=columna

    def setValue(self, value: Expression):
        self.value = value

    def execute(self, environment: Environment):

        try:
            tempValue = self.value.execute(environment)

            if(self.type.value != tempValue.getType().value):
                if self.type.value!=5:
                    print("Los tipos no coinciden")
                    environment.saveParameter('None',Primitive(0,typeExpression.INTEGER,self.linea,self.columna).execute(environment),typeExpression.INTEGER,False,self.linea,self.columna)
                    return
                else:
                    self.type=tempValue.getType()

            environment.saveVariable(self.id,tempValue,self.type, False,self.linea, self.columna)

        except:
            print("\nError al procesar parámetros!")
            Listas.saveError("Error al procesar parámetros!",self.linea,self.columna)
            
        