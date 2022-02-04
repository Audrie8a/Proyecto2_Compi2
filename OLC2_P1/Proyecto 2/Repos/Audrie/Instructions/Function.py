
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Environment.Listas import Listas

class Function(Instruction):
    
    def __init__(self, id: str, parameters,block,linea,columna) -> None:
        super().__init__()
        self.id = id
        self.parameters = parameters
        self.block = block
        self.linea=linea
        self.columna=columna

    def compile(self, environment: Environment):
        tama=1
        if self.parameters!=None:
            tama=len(self.parameters)+1

        environment.saveFunction(self.id,self,str(tama),self.linea,self.columna)
        #Nombre - Visibilidad - Ambito -> Lo que se necesita para editar
        #Listas.saveTabla("hola","string",environment.Nombre,"global",str(tama),"~","function")

    def executeFunction(self, environment: Environment):
        try:
            newEnv = environment#Environment(environment, environment.Nombre+"~"+self.id)
            codigo3d=""

            
            Listas.lstFunciones.append([self.id,environment.father.Nombre, "func "+self.id+"(){\n"])
            

            # Compila expresiones
            for parameter in self.parameters:
                parameter.compile(newEnv)
            
            number=0
            while number< len( self.block):
                Listas.function=Listas.function+1
                Listas.FunctionActiva=True
                
                ins=self.block[number]
                if hasattr(ins,"id"):
                    if ins.id=='return':
                            temporal = ins.value.compile(environment)
                            return #Symbol("",temporal.getValue(),temporal.getType(),"",self.linea,self.columna)
                    elif ins.id=='continue' or ins.id=='break':
                        print("\nError continue o break están fuera de un ciclo ",self.linea,self.columna)
                        Listas.saveError("Error continue o break están fuera de un ciclo",self.linea,self.columna)
                        return #Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)
                respuesta=ins.compile(newEnv)
                if respuesta!=None:
                        if respuesta[0]=='return':
                            return respuesta[1]
                number = number+1
            
            Listas.function=Listas.function-1
            Listas.FunctionActiva=False
            fin=len(Listas.lstFunciones)
            Listas.lstFunciones[fin-1][2]=Listas.lstFunciones[fin-1][2]+"}\n"

        except:
            fin=len(Listas.lstFunciones)-1
            Listas.lstFunciones[fin]=""
            print("\n Error al ejecutar funcion!")
            Listas.saveError("Error al ejecutar función!",self.linea,self.columna)

    def executeFunctionNone(self, environment: Environment):
        try:
            newEnv = Environment(environment, environment.Nombre+"~"+self.id)
            codigo3d=""

            
            Listas.lstFunciones.append([self.id,environment.father.Nombre, "func "+self.id+"(){\n"])
            
            number=0
            while number<len(self.block):
                Listas.function=Listas.function+1
                Listas.FunctionActiva=True

                ins=self.block[number]
                if hasattr(ins,"id"):
                    if ins.id=='return':
                        temporal = ins.value.compile(environment)
                        return #Symbol("",temporal.getValue(),temporal.getType(),"",self.linea,self.columna)                            
                    elif ins.id=='continue' or ins.id=='break':
                        print("\nError continue o break están fuera de un ciclo ",self.linea,self.columna)
                        Listas.saveError("Error continue o break están fuera de un ciclo",self.linea,self.columna)
                        return #Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)
                
                respuesta=ins.compile(newEnv)

                

                if respuesta!=None:
                        if respuesta[0]=='return':
                            return respuesta[1]
                number = number+1
            
            Listas.function=Listas.function-1
            Listas.FunctionActiva=False
            fin=len(Listas.lstFunciones)
            Listas.lstFunciones[fin-1][2]=Listas.lstFunciones[fin-1][2]+"}\n"
        except:
            fin=len(Listas.lstFunciones)-1
            Listas.lstFunciones[fin]=""
            print("\nError al ejecutar funcion!")
            Listas.saveError("Error al ejecutar función!",self.linea,self.columna)