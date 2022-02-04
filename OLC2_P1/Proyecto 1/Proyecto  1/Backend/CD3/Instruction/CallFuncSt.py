from Environment.Symbol import Symbol
from Instruction.Parameter import Parameter
from Instruction.Function import Function
from Instruction.DecStruct import DecStruct
from Instruction.atributosStruct import atributosStruct
from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas


class CallFuncSt(Instruction):

    def __init__(self,id,parameters,linea,columna) -> None:
        self.id = id
        self.parameters = parameters
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        
        
        repons= environment.getFunction(self.id,self.linea,self.columna)
        if repons[0]=="Struct":
            tempFunc: DecStruct = repons[1]
            contador=0
            if len(tempFunc.blockAtributos)==len(self.parameters):
                for atrb in tempFunc.blockAtributos:
                    tempValue = self.parameters[contador].execute(environment)
                    if(atrb.type!=tempValue.getType() and atrb.type!=typeExpression.OBJETO):
                            print("\n Error al instanciar struct, verifique que los tipos de datos ingresados!")
                            Listas.saveError("Error al instanciar struct, verifique que los tipos de datos ingresados!",self.linea,self.columna)
                            return None
                    
                    contador=contador+1 
                return ["Struct",self.parameters,self.id,tempFunc.tipoStruct,environment]
            else:
                print("\n Error al instanciar struct, verifique que los datos coincidan con los atributos del struct!")
                Listas.saveError("Error al instanciar struct, verifique que los datos coincidan con los atributos del struct!",self.linea,self.columna)
                return None     
        else:
            tempFunc: Function =repons[1]

            newEnvironment = Environment(environment.getGlobal(),"Llamada Funcion "+self.id)
            try:
                if tempFunc.parameters!=None:            
                    for x in range(0,len(tempFunc.parameters)):
                        tempPar: Parameter = tempFunc.parameters[x]
                        tempPar.setValue(self.parameters[x])

                    respuesta=tempFunc.executeFunction(newEnvironment)
                    if respuesta!= None:
                        return respuesta
                else:
                    respuesta=tempFunc.executeFunctionNone(newEnvironment)
                    if respuesta!= None:
                        return respuesta
            except:
                print("\n Error al procesar función, verifique parámetros!")
                Listas.saveError("Error al procesar función, verifique parámetros!",self.linea,self.columna)
            
    def InstanciarStruct(variable,tipo,parametros,id,entorno,linea,columna):
            #repons= entorno.getFunction(id,linea,columna)
            entorno.instanceStruct(entorno.Struct,variable,tipo,parametros,id,linea,columna)
            Listas.saveTabla(variable,"Struct",tipo,linea,columna)
            