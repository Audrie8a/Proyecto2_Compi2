from typing import List
from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Environment import Environment
from Abstract.Instruction import Instruction
from Abstract.Expression import Expression
from Environment.Listas import Listas

class ifSt(Instruction):

    def __init__(self, condition: Expression, block, elseBlock,fila,columna) -> None:
        self.condition = condition
        self.block = block
        self.elseBlock = elseBlock
        self.line=fila
        self.column=columna

    def execute(self, environment: Environment):
        
        tempCondition: Symbol = self.condition.execute(environment)

        if tempCondition.getType()!= typeExpression.BOOL:
            print("Condición de tipo no boolean")
            Listas.saveError("Condición de tipo no booleano",self.line,self.column)
            
        
        if(tempCondition.getValue() == True):
            for ins in self.block:
                if hasattr(ins,"id"):
                    if ins.id=='continue':
                        if Listas.cicloWhile==True or Listas.cicloFor==True:
                            return ['continue',0]
                        else:
                            Listas.saveError("continue, No se encuentra dentro de un ciclo",self.line,self.column)
                            print("Continue, No se encuentra dentro de un ciclo",self.line,self.column)
                            return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]
                    elif ins.id=='return':
                        if Listas.function==True:

                            Listas.retornar=True
                            
                            temporal=ins.value.execute(environment)
                            return ['return',Symbol("",temporal.getValue(),temporal.getType(),"",self.line,self.column)]
                        else:
                            Listas.saveError("return, No se encuentra dentro de una funcion",self.line,self.column)
                            print("return, No se encuentra dentro de una funcion",self.line,self.column)
                            return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]
                    elif ins.id == 'break':
                        if Listas.cicloFor==True or Listas.cicloWhile==True:
                            Listas.romper=True
                            temporal=ins.value.execute(environment)
                            return ['break',Symbol("",temporal.getValue(),temporal.getType(),"",self.line,self.column)]
                        else:
                            Listas.saveError("break, No se encuentra dentro de un ciclo",self.line,self.column)
                            print("break, No se encuentra dentro de un ciclo",self.line,self.column)
                            return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]

                ins.execute(environment)
        elif self.elseBlock!=None:
            try:
                for ins in self.elseBlock:
                    if hasattr(ins,"id"):
                        if ins.id=='continue':
                            if Listas.cicloWhile==True or Listas.cicloFor==True:
                                return ['continue',0]
                            else:
                                Listas.saveError("continue, No se encuentra dentro de un ciclo",self.line,self.column)
                                print("Continue, No se encuentra dentro de un ciclo",self.line,self.column)
                                return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]
                        elif ins.id=='return':
                            if Listas.cicloFor==True or Listas.cicloWhile==True  or Listas.function==True:

                                Listas.retornar=True
                                aux=ins.value
                                if hasattr(aux,"operation"):
                                    tempValue = aux.execute(environment)
                                    return ['return',Symbol("",tempValue.value,tempValue.type,"",self.line,self.column)]
                                elif hasattr(aux,"id"):
                                    retValue = environment.getVariable(aux.id,self.line,self.column)
                                    return ['return',Symbol("",retValue.value,retValue.type,"",self.line,self.column)]
                                else:
                                    return ['return',Symbol("",ins.value.value,ins.value.type,"",self.line,self.column)]
                            else:
                                Listas.saveError("return, No se encuentra dentro de un ciclo",self.line,self.column)
                                print("return, No se encuentra dentro de un ciclo",self.line,self.column)
                                return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]
                        elif ins.id == 'break':
                            if Listas.cicloFor==True or Listas.cicloWhile==True:
                                Listas.romper=True
                                return ['break',Symbol("",ins.value.value,ins.value.type,"",self.line,self.column)]
                            else:
                                Listas.saveError("break, No se encuentra dentro de un ciclo",self.line,self.column)
                                print("break, No se encuentra dentro de un ciclo",self.line,self.column)
                                return ['return',Symbol("",0,typeExpression.INTEGER,"",self.line,self.column)]
                ins.execute(environment)
            except:
                if hasattr(self.elseBlock,"block") and hasattr(self.elseBlock,"elseBlock"):
                    self.condition=self.elseBlock.condition
                    self.block=self.elseBlock.block
                    self.elseBlock=self.elseBlock.elseBlock
                    respuesta=self.execute(environment)
                    return respuesta
                elif hasattr(self.elseBlock,"block"):
                    self.condition=self.elseBlock.condition
                    self.block=self.elseBlock.block
                    self.elseBlock=None
                    respuesta=self.execute(environment)
                    return respuesta

