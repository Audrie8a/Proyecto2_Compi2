from os import error
from Environment.Symbol import Symbol
from Environment.Environment import Environment
from Abstract.Instruction import Instruction
from Abstract.Expression import Expression
from Environment.Listas import Listas

class While(Instruction):

    def __init__(self, condition: Expression, block,linea,columna) -> None:
        self.condition = condition
        self.block = block
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        try:

            tempCondition: Symbol = self.condition.execute(environment)

            while(tempCondition.getValue() == True or tempCondition.getValue()=='true' ):
                
                newEnv = Environment(environment, environment.nombre+"While")
                number=0
                while number<(len(self.block)):
                    ins=self.block[number]
                    Listas.cicloWhile=True
                    if hasattr(ins,"id"):
                        temporal= ins.value.execute(environment)
                        if ins.id=='continue':
                            continue
                        elif ins.id=='return':                            
                            print("\nError no se puede declarar un return en un while! ",self.linea,self.columna)
                            Listas.saveError("Error no se puede declarar un return en un while!",self.linea,self.columna)
                            return None
                            
                        elif ins.id == 'break':
                            return['return', Symbol("",temporal.getValue(),temporal.getType(),"",self.linea,self.columna)]
                        
                    respuesta=ins.execute(newEnv)
                    if respuesta!=None:
                        if respuesta[0]=='continue':
                            number=number+1
                        elif respuesta[0]=='return':
                            return respuesta
                        elif respuesta[0]=='break':
                            return respuesta
                    
                    number=number+1

                tempCondition = self.condition.execute(environment)

            Listas.cicloWhile=False
            Listas.continuar=False
            Listas.retornar=False
            Listas.romper=False
        except(error):
            print(error)
            print("\nError al ejecutar el while ",self.linea,self.columna)
            Listas.saveError("Error al ejecutar el while!",self.linea,self.columna)