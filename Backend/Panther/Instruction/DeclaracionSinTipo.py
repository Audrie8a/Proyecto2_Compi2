from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Enum.Dominant import Dominant
from Enum.DominantRelatonal import DominantRelational

class DeclaracionSinTipo(Instruction):
     listOperations=['MAYORQ','MENORQ','MAYORIGUAL','MENORIGUAL','IGUALIGUAL','DIFERENTE']
     def __init__(self,tipoVariable, id: str,value: Expression, isArray: bool, linea, columna) -> None:
        self.tipoVariable=tipoVariable
        self.id = id
        try:
           self.type =value.type
        except:
           self.type=typeExpression.OBJETO
        self.value = value
        self.isArray = isArray
        self.linea=linea
        self.columna = columna
    
     def execute(self, environment: Environment):
       
        tempValue = self.value.execute(environment)
        if(self.type.value != tempValue.getType().value):
           if self.type.value!=5:
              print("Los tipos no coinciden")
              environment.saveVariable('None',Primitive(0,typeExpression.INTEGER).execute(environment),typeExpression.INTEGER,False,self.linea, self.columna)
              return
           else:
              self.type=tempValue.getType()

        if self.tipoVariable=='global':
            environment.getGlobal().saveVariableGlobal(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
        elif self.tipoVariable=='local':
            environment.saveVariable(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
        else:
            environment.saveVariable(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
        
    