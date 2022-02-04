
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Environment.Symbol import Symbol
from Environment.Listas import Listas

class IPrint(Instruction):

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
                print("[", end=" ")
                Listas.saveSalida("[","print")

                for variable in aux:
                    self.imprimirValores(env,variable)

                print("]", end=" ")
                Listas.saveSalida("]","print")
                return

        except:
            print(aux.getValue(), end=" ")
            Listas.saveSalida(aux.getValue(),"print")
            return