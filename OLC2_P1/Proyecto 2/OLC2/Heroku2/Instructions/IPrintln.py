from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas
from Instructions.IPrint import IPrint

class IPrintln(Instruction):

    def __init__(self, exp: Expression) -> None:
        super().__init__()
        self.exp = exp

    def compile(self, environment: Environment) -> Value:

        # Si es una lista 
        if hasattr(self.exp,"generator")==False:
            self.ImprimirListado(environment,self.exp)
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
            IPrintln.ImprimirStrings(self,tempValue)

        else:
            print("Error en println")
            Listas.saveError("Error en println",0,0)

        self.generator.addNewLine()


    def ImprimirListado(self, entorno:Environment, lista):       
        for ins in lista:
            if hasattr(ins,"generator")==False:
                self.ImprimirListado(entorno)
                return;

            ins.generator = self.generator
        
            tempValue: Value = ins.compile(entorno)

            if(tempValue.type == typeExpression.INTEGER):
                self.generator.addPrintf("d","int(" + str(tempValue.getValue())+")")

            elif(tempValue.type == typeExpression.FLOAT):
                self.generator.addPrintf("f", str(tempValue.getValue()))

            elif(tempValue.type == typeExpression.BOOL):
                Impresiones.imprimirBooleans(self.generator,tempValue.getValue())
            elif(tempValue.type == typeExpression.STRING):
                IPrintln.ImprimirStrings(self,tempValue)
                
            else:
                print("Error en println")
                Listas.saveError("Error en println",0,0)


    def ImprimirStrings(self,tempValue):
        condicion=False
        for c in tempValue.value:
            if c=='~':
                condicion=True
                break
        if condicion:
            aux=tempValue.value.split("~",2)
            cadena=aux[0]
            temp = aux[1]
            if(tempValue.isTemp):
                if aux[2]=='':
                    Impresiones.imprimirCadenasPotenciaPosicion(self.generator,cadena,temp)
                else:
                    Impresiones.imprimirCadenasPotenciaPosicion(self.generator,cadena,temp)
                    IPrintln.ImprimirStrings(self,aux[2])
            else:
                if aux[2]=='':
                    Impresiones.imprimirCadenasPotencia(self.generator,cadena,temp)
                else:
                    Impresiones.imprimirCadenasPotencia(self.generator,cadena,temp)
                    IPrintln.ImprimirStrings(self,aux[2])
        else:
            if(tempValue.isTemp):
                Impresiones.imprimirCadenasPosicion(self.generator,tempValue.value)
            else:
                Impresiones.imprimirCadenas(self.generator,tempValue.value)
        
                

                
            
            
              
