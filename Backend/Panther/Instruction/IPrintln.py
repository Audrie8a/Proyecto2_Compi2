
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Environment.Symbol import Symbol

class IPrintln(Instruction):

    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def execute(self, environment: Environment):
        tempExp = self.expression.execute(environment)
        print("")
        print(tempExp.getValue(), end=" ")
        