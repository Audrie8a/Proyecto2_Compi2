from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Listas import Listas
from Environment.Value import Value
from Enum.typeExpression import typeExpression


class whileSt(Instruction):

    def __init__(self, condition: Expression, block, linea, columna) -> None:
        self.condition = condition
        self.block = block
        self.line=linea
        self.column=columna
    
    def compile(self, environment: Environment) -> Value:
        
        self.condition.generator = self.generator
        L0 = self.generator.newLabel()
        L1= self.generator.newLabel()
        
        self.generator.addLabel(L0) #L0:

        valueCondition = self.condition.compile(environment)

        if(valueCondition.type == typeExpression.BOOL):
                

            Nombre="While"+str(self.line)+"-"+str(self.column)
            newEnv = environment #Environment(environment,Nombre)
            self.generator.addIf(valueCondition.value,"0","==",L1)   
            for ins in self.block:
                ins.generator = self.generator
                ins.compile(newEnv)

            # valueCondition=nuevo Valor
            valueCondition2 = self.condition.compile(environment)
            self.generator.addExpression(valueCondition.value,valueCondition2.value,"","")
            self.generator.addGoto(L0)
            self.generator.addLabel(L1)
        else:
            print("ERROR EN WHILE")
            Listas.saveError("Error en While",self.line,self.column)