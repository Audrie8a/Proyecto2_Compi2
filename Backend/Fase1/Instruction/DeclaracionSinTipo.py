from Instruction.CallFuncSt import CallFuncSt
from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Enum.Dominant import Dominant
from Enum.DominantRelatonal import DominantRelational
from Environment.Listas import Listas

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
        try:
         tempValue = self.value.execute(environment) # Hacer un arreglo que devuelva si es funcion o instancia, si es isntancia saltarse todos los pasos de abajo
         try:
            if len(tempValue)!=0:
               CallFuncSt.InstanciarStruct(self.id,tempValue[3],tempValue[1],tempValue[2],tempValue[4],self.linea,self.columna)
         except:
            if(self.type.value != tempValue.getType().value):
                  if self.type.value!=5:
                     print("\nLos tipos no coinciden")
                     environment.saveVariable("",Primitive(0,typeExpression.INTEGER,self.linea,self.columna),typeExpression.INTEGER,False, self.linea, self.columna)
                     Listas.saveError("Los tipos no coinciden",self.linea,self.columna)
                     return
                  else:
                     self.type=tempValue.getType()
               
            if self.tipoVariable=='global':
               environment.getGlobal().saveVariableGlobal(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
            elif self.tipoVariable=='local':
               environment.saveVariableLocal(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
            else:
               environment.saveVariable(self.id,tempValue,self.type,self.isArray,self.linea, self.columna)
        except:
           print("\n Error al realizar declaración variable!")
           Listas.saveError("Error al realizar declaración variable!",self.linea,self.columna)

class SoloDeclaracion(Instruction):
     def __init__(self,tipoVariable, id: str,isArray: bool, linea, columna) -> None:
        self.tipoVariable=tipoVariable
        self.id = id
        self.isArray = isArray
        self.linea=linea
        self.columna = columna
    
     def execute(self, environment: Environment):
        if self.tipoVariable=='local':
            environment.saveVariableLocal(self.id,0,typeExpression.OBJETO,False,self.linea, self.columna)
        else:
            environment.getGlobal().saveVariableGlobal(self.id,0,typeExpression.OBJETO,False,self.linea, self.columna)
                    
    