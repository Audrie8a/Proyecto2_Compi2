from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Listas import Listas

class arreglo(Instruction):

    def __init__(self,id,lstVal,type,linea, columna) -> None:
        self.id=id
        self.lstVal=lstVal
        self.type=type
        self.linea=linea
        self.columna = columna
        

    def execute(self, environment: Environment):
        
        try:            
            lstValores=[]
            for ins in self.lstVal:
                lstValores.append(self.convertirValores(environment,ins))
                #val=ins.execute(environment)
                #lstValores.append(val)
            self.lstVal=lstValores
            environment.saveArreglo(self.id,self,self.linea,self.columna)
            self.longitud=len(self.lstVal)
            
        except:
            print("\n Error al realizar declaración arreglo!")
            Listas.saveError("Error al realizar declaración arreglo!",self.linea,self.columna)
    

    def convertirValores(self, env:Environment, ins):
        aux=ins
        try:
            if len(aux)!=-1:
                temporal=[]
                for variable in aux:
                    temporal.append(self.convertirValores(env,variable))
                
                aux=temporal
                return aux
        except:
            aux=aux.execute(env)
            return aux

    