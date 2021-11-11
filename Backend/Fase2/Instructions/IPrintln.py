from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas

class IPrintln(Instruction):

    def __init__(self, exp: Expression) -> None:
        super().__init__()
        self.exp = exp

    def compile(self, environment: Environment) -> Value:

        # Si es una lista 
        if hasattr(self.exp,"generator")==False:
            self.ImprimirListado(self,self.exp)
            self.generator.addNewLine()
            return
      

        # Si no es una lista
        self.exp.generator = self.generator
        
        tempValue: Value = self.exp.compile(environment)

        if(tempValue.type == typeExpression.INTEGER):
            self.generator.addPrintf("d","int(" + str(tempValue.getValue())+")")

        elif(tempValue.type == typeExpression.FLOAT):
            self.generator.addPrintf("f", str(tempValue.getValue()))

        elif(tempValue.type == typeExpression.BOOL):
            Impresiones.imprimirBooleans(self.generator,tempValue.getValue())
        elif(tempValue.type == typeExpression.STRING):
            aux= len(tempValue.value)-1
            if tempValue.value[aux]=='~':
                Impresiones.imprimirCadenasPotencia(self.generator,tempValue.value)
            else:
                Impresiones.imprimirCadenas(self.generator,tempValue.value)

        else:
            print("Error en println")
            Listas.saveError("Error en println",0,0)

        self.generator.addNewLine()


    def ImprimirListado(compilador, entorno, lista):       
        for ins in lista:
            if hasattr(ins,"generator")==False:
                compilador.ImprimirListado(entorno,ins)
                return;

            ins.generator = compilador.generator
        
            tempValue: Value = ins.compile(entorno)

            if(tempValue.type == typeExpression.INTEGER):
                compilador.generator.addPrintf("d","int(" + str(tempValue.getValue())+")")

            elif(tempValue.type == typeExpression.FLOAT):
                compilador.generator.addPrintf("f", str(tempValue.getValue()))

            elif(tempValue.type == typeExpression.BOOL):
                Impresiones.imprimirBooleans(compilador.generator,tempValue.getValue())
            elif(tempValue.type == typeExpression.STRING):
                aux= len(tempValue.value)-1
                if tempValue.value[aux]=='~':
                        Impresiones.imprimirCadenasPotencia(compilador.generator,tempValue.value)
                else:
                        Impresiones.imprimirCadenas(compilador.generator,tempValue.value)

            else:
                print("Error en println")
                Listas.saveError("Error en println",0,0)
            
            
              
