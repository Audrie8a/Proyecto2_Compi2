from Expression.Primitive import Primitive
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Listas import Listas

class length(Instruction):

    def __init__(self,id,linea, columna) -> None:
        self.id=id
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        
        try: 
            self.id=self.id.execute(environment)
            long = len(self.id)        
            return Symbol("",long,typeExpression.INTEGER,"",self.linea,self.columna)
            
        except:
            try:
                long=environment.getLengthArreglo(self.id,self.linea,self.columna)
                return long
            except:                
                print("\n Error al obtener tamaño arreglo!")
                Listas.saveError("Error al obtener tamaño arreglo!",self.linea,self.columna)
    

   