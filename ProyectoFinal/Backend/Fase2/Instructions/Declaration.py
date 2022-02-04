from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas


class Declaration(Instruction):

    def __init__(self,tipoVariable, id:str, exp: Expression, type: typeExpression) -> None:
        super().__init__()
        self.tipoVariable=tipoVariable
        self.id = id
        self.exp = exp
        self.type = type

    def compile(self, environment: Environment) -> Value:

        if self.exp=="null":
            Declaration.SinValorInicial(self,environment)
        else:
            Declaration.ValorInicial(self,environment)      



    def ValorInicial(self, environment: Environment):

        self.exp.generator = self.generator
        
        newValue: Value = self.exp.compile(environment)
        index=self.generator.PointerFree(0)

        if self.type!=newValue.type:
            if self.type!= typeExpression.OBJETO:
                print("\nLos tipos no coinciden")
                Listas.saveError("Los tipos no coinciden",self.linea,self.columna)
                return
            else:
                self.type=newValue.type
        

        tamaIni=len(Listas.getListError())

        if self.tipoVariable=="local":
            tempVar: Symbol = environment.saveVariableLocal(self.id,self.type,"1",str(index),newValue)
        elif self.tipoVariable=="global":
            tempVar: Symbol = environment.saveVariableGlobal(self.id,self.type,"1",str(index),newValue)
        else:
            tempVar: Symbol = environment.saveVariable(self.id,self.type,"1",str(index),newValue)
        
        if len(Listas.getListError())==tamaIni:
            if self.type==typeExpression.INTEGER or self.type==typeExpression.FLOAT or self.type==typeExpression.BOOL:
                Impresiones.saveVariable3D(self.generator,environment.Nombre,self.tipoVariable,self.id,str(newValue.value),self.type,str(index),"numeros")
            elif self.type==typeExpression.STRING or self.type==typeExpression.CHAR: 
                Impresiones.saveVariable3D(self.generator,environment.Nombre,self.tipoVariable,self.id,str(newValue.value),self.type,str(index),"letras")
    
    
    def SinValorInicial(self, environment: Environment):
        print("")
