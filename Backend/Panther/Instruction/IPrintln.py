
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
            print("")
            print(tempExp.getValue(), end=" ")
            Listas.saveSalida(tempExp.getValue(),"println")
        except:
            print("\nError al imprimir",self.linea,self.columna)
            Listas.saveError("Error al imprimir!",self.linea,self.columna)
        