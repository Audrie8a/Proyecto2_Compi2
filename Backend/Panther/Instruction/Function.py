
from Instruction.Parameter import Parameter
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression

class Function(Instruction):
    
    def __init__(self, id: str, parameters,block) -> None:
        self.id = id
        self.parameters = parameters
        self.block = block

    def execute(self, environment: Environment):
        environment.saveFunction(self.id,self)

    def executeFunction(self, environment: Environment):

        newEnv = Environment(environment)
        for parameter in self.parameters:
            parameter.execute(newEnv)
        
        for ins in self.block:
            ins.execute(newEnv)

    def executeFunctionNone(self, environment: Environment):

        newEnv = Environment(environment)
        
        for ins in self.block:
            ins.execute(newEnv)