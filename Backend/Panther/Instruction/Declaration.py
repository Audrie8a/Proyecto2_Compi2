from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression

class Declaration(Instruction):

    def __init__(self,tipoVariable, id: str, type: typeExpression, value: Expression, isArray: bool, linea, columna) -> None:
        self.tipoVariable=tipoVariable
        self.id = id
        self.type = type
        self.value = value
        self.isArray = isArray
        self.linea=linea
        self.columna = columna

    def execute(self, environment: Environment):
        
        if self.tipoVariable=='global':
            print("Global");
        elif self.tipoVariable=='local':
            print("Local")
        else:
            print("Normal")
            
        tempValue = self.value.execute(environment)

        if(self.type.value != tempValue.getType().value):
            print("Los tipos no coinciden")
            environment.saveVariable('None',Primitive(0,typeExpression.INTEGER).execute(environment),typeExpression.INTEGER, self.linea, self.columna)
            return

        environment.saveVariable(self.id,tempValue,self.type,self.isArray, self.linea, self.columna)
    

