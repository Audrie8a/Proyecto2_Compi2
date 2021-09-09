from Instruction.Parameter import Parameter
from Instruction.Function import Function
from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression

class CallFuncSt(Instruction):

    def __init__(self,id,parameters,linea,columna) -> None:
        self.id = id
        self.parameters = parameters
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        
        tempFunc: Function = environment.getFunction(self.id,self.linea,self.columna)
        newEnvironment = Environment(environment.getGlobal())
        try:
            if tempFunc.parameters!=None:            
                for x in range(0,len(tempFunc.parameters)):
                    tempPar: Parameter = tempFunc.parameters[x]
                    tempPar.setValue(self.parameters[x])

                tempFunc.executeFunction(newEnvironment)
            else:
                tempFunc.executeFunctionNone(newEnvironment)
        except:
            print("\n Error al procesar función, verifique parámetros!")