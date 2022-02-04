from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas

class ifSt(Instruction):

    def __init__(self, condition: Expression, block, elseBlock,fila,columna) -> None:
        super().__init__()
        self.condition = condition
        self.block = block
        self.elseBlock = elseBlock
        self.line=fila
        self.column=columna

    def compile(self, environment: Environment) -> Value:
        
        self.exp.generator = self.generator

        tempCondition: Value = self.condition.compile(environment)

        if tempCondition.type != typeExpression.BOOL:
            print("Condición de tipo no boolean")
            Listas.saveError("Condición de tipo no booleano",self.line,self.column)
            return
        

    def ImprimirIf(self,environment, tempCondition):
        L0=self.generator.newLabel()
        L1=self.generator.newLabel()
        self.generator.addIf(tempCondition,"","",L0)
        self.generator.addGoto(L1)
        self.generator.addLabel(L0)
        
        #Ejecutar Instrucciones
        self.block.compile(environment)

        self.generator.addLabel(L1)

        if self.elseBlock!=None:
            print("")
         
        