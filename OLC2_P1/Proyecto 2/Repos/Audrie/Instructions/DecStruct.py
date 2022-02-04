from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Listas import Listas
class DecStruct(Instruction):

    def __init__(self,tipoStruct,id,blockAtributos,linea, columna) -> None:
        self.tipoStruct=tipoStruct
        self.id=id
        self.blockAtributos=blockAtributos
        self.linea=linea
        self.columna = columna
        self.instancias=[]

    def compile(self, environment: Environment):
        
        try:
            lstAtributos=[]
            for ins in self.blockAtributos:
                lstAtributos.append(ins)

            environment.saveStruct(self.id,self,self.linea,self.columna)
            lstAtributos.clear()
        except:
            print("\n Error al realizar declaración variable!")
            Listas.saveError("Error al realizar declaración variable!",self.linea,self.columna)
    

