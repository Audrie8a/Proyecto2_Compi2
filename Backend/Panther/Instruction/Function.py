
from Environment.Symbol import Symbol
from Instruction.Parameter import Parameter
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas

class Function(Instruction):
    
    def __init__(self, id: str, parameters,block,linea,columna) -> None:
        self.id = id
        self.parameters = parameters
        self.block = block
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        environment.saveFunction(self.id,self,self.linea,self.columna)

    def executeFunction(self, environment: Environment):
        try:
            newEnv = Environment(environment, "Funcion "+self.id)
            for parameter in self.parameters:
                parameter.execute(newEnv)
            
            number=0
            while number< len( self.block):
                Listas.function=True
                ins=self.block[number]
                if hasattr(ins,"id"):
                    if ins.id=='return':
                            
                            return Symbol("",ins.value,ins.value.type,"",self.linea,self.columna)
                    elif ins.id=='continue' or ins.id=='break':
                        print("\nError continue o break están fuera de un ciclo ",self.linea,self.columna)
                        Listas.saveError("Error continue o break están fuera de un ciclo",self.linea,self.columna)
                        return Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)
                respuesta=ins.execute(newEnv)
                if respuesta!=None:
                        if respuesta[0]=='return':
                            return respuesta[1]
                number = number+1
            
            Listas.function=False
        except:
            print("\n Error al ejecutar funcionnnn!")
            Listas.saveError("Error al ejecutar función!",self.linea,self.columna)

    def executeFunctionNone(self, environment: Environment):
        try:
            newEnv = Environment(environment,"Funcion "+self.id)
            
            number=0
            while number<len(self.block):
                Listas.function=True
                ins=self.block[number]
                if hasattr(ins,"id"):
                    if ins.id=='return':
                        try:
                            return Symbol("",ins.value.value,ins.value.type,"",self.linea,self.columna)
                        except:
                            return Symbol("",ins.value,ins.value.type,"",self.linea,self.columna)
                            
                    elif ins.id=='continue' or ins.id=='break':
                        print("\nError continue o break están fuera de un ciclo ",self.linea,self.columna)
                        Listas.saveError("Error continue o break están fuera de un ciclo",self.linea,self.columna)
                        return Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)
                respuesta=ins.execute(newEnv)
                if respuesta!=None:
                        if respuesta[0]=='return':
                            return respuesta[1]
                number = number+1
            
            Listas.function=False
        except:
            print("\nError al ejecutar funcion!")
            Listas.saveError("Error al ejecutar función!",self.linea,self.columna)