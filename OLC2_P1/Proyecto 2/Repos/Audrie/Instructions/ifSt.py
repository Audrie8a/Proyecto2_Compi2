from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas
from Instructions.block import block

class ifSt(Instruction):

    def __init__(self, condition: Expression, block, elseBlock,fila,columna) -> None:
        super().__init__()
        self.condition = condition
        self.block = block
        self.elseBlock = elseBlock
        self.line=fila
        self.column=columna

    def compile(self, environment: Environment) -> Value:
        
        
        L0=self.generator.newLabel()
        L1=self.generator.newLabel()
        Lfinal=self.generator.newLabel()
        ifSt.ImprimirIf(self,environment,self.condition, self.block,self.elseBlock,L0,L1,Lfinal,self.line,self.column)
        self.generator.addLabel(Lfinal)
        
        

    def ImprimirIf(self,environment, condition, block, elseBlock, L0,L1,Salida,fila, columna):
        
        try:
            condition.generator = self.generator

            tempCondition: Value = condition.compile(environment)
            

            if tempCondition.type != typeExpression.BOOL:
                print("Condición de tipo no boolean")
                Listas.saveError("Condición de tipo no booleano",fila,columna)
                return

            
            self.generator.addIf(tempCondition.value,"1","==",L0)
            if elseBlock==None and hasattr(elseBlock,"block")==False:
                self.generator.addGoto(Salida)
            else:
                self.generator.addGoto(L1)

            self.generator.addLabel(L0)
            #Ejecutar Instrucciones
            for ins in block:
                ins.generator=self.generator
                ins.compile(environment)
            

            if elseBlock!=None:
                self.generator.addGoto(Salida) 
                self.generator.addLabel(L1)
                if hasattr(elseBlock,"block"):        #Si es un else if        
                    L0N=self.generator.newLabel()
                    L1N=self.generator.newLabel()
                    ifSt.ImprimirIf(self,environment,elseBlock.condition,elseBlock.block,elseBlock.elseBlock,L0N,L1N,Salida,fila,columna)
                    
                    return
                else:     # Si es un else           
                    for ins in elseBlock:
                        ins.generator=self.generator
                        ins.compile(environment)
                    self.generator.addGoto(Salida)

                    
                    
            else:   # Si no existe else
                self.generator.addGoto(L1)
                self.generator.addLabel(L1)
            
           
        except:
            print("Error al compilar If",fila,columna)
            Listas.saveError("Error al compilar If",fila,columna)
        
        
  