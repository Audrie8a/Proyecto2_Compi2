from Environment.Symbol import Symbol
from Enum.typeExpression import typeExpression
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas
from Environment.Value import Value

class Parameter (Instruction):
    def __init__(self, id: str, type: typeExpression,linea, columna) -> None:
        super().__init__()
        self.id = id
        self. type = type
        self.value = None
        self.linea=linea
        self.columna=columna
    
    def setValue(self, value: Expression):
        self.value = value
    
    def compile(self, environment: Environment):

        try:
            self.value.generator = self.generator
            tempValue: Value = self.value.compile(environment)
            index=Listas.searchTabla(self.id,environment.Nombre)
            if index=="empty":
                index= self.generator.PointerFree(0)
            else:
                index=index[5]

            if(self.type != tempValue.type):
                if self.type!=typeExpression.OBJETO:
                    print("Los tipos no coinciden")
                    Listas.saveError("Los tipos no coiciden",self.linea,self.columna)
                    return
                else:
                    self.type=tempValue.type

            tamaIni=len(Listas.getListError())
            tempVar: Symbol= environment.saveVariable(self.id,self.type,"1",str(index),tempValue,"parameter")
            
            if len(Listas.getListError())==tamaIni:
                if self.type==typeExpression.INTEGER or self.type==typeExpression.FLOAT or self.type==typeExpression.BOOL:
                    Impresiones.saveVariable3D(self.generator,tempVar.Ambito,tempVar.Visibilidad,tempVar.id,tempValue.value,tempVar.Tipo,tempVar.Position,"numeros")
                elif self.type==typeExpression.STRING or self.type==typeExpression.CHAR: 
                    Impresiones.saveVariable3D(self.generator,tempVar.Ambito,tempVar.Visibilidad,tempVar.id,tempValue.value,tempVar.Tipo,tempVar.Position,"letras")
    
        except:
            print("\nError al procesar parámetros!")
            Listas.saveError("Error al procesar parámetros!",self.linea,self.columna)