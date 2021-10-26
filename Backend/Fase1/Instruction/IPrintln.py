
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Environment.Symbol import Symbol
from Environment.Listas import Listas
class IPrintln(Instruction):

    def __init__(self, expression: Expression,linea,columna) -> None:
        self.expression = expression
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment):
        try:
            tempExp = self.expression.execute(environment)
            self.imprimirValores(environment,tempExp)
        except:
            print("\nError al imprimir",self.linea,self.columna)
            Listas.saveError("Error al imprimir!",self.linea,self.columna)
        
    def imprimirValores(self, env:Environment, ins):
        aux=ins
        try:
            if len(aux)!=-1:
                print("")
                print("[", end=" ")
                Listas.saveSalida("[","println")

                for variable in aux:
                    self.imprimirValores(env,variable)
                    
                print("")
                print("]", end=" ")
                Listas.saveSalida("]","println")
                return

        except:
            print("")
            print(aux.getValue(), end=" ")
            Listas.saveSalida(aux.getValue(),"println")
            return
