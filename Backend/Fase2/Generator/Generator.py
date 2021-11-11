from typing import List
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas
class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.tempList = []
        self.tamaStack=30101999
        self.P=0
        self.H=0

    #Obtener los temporales usados
    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)
    

    #Obtener el codigo generado
    def getCode(self) -> str:
        metodoPow=Impresiones.PotenciaAux
        metodoPrint=Impresiones.PrintAux
        metodoPowString=Impresiones.PotenciaStrAux
        metodoMod=Impresiones.ModAux
       
        tempCode: str = 'package main;\n'
        tempCode = tempCode + 'import("fmt");\n'
        tempCode = tempCode + "var P, H float64;\n"
        tempCode = tempCode + "var stack[78000]float64;\n"
        tempCode = tempCode + "var heap["+str(self.H)+"]float64;\n"


        if(len(self.tempList) > 0):
            tempCode = tempCode + "var " + self.getUsedTemps() + " float64;\n\n"

        #Funciones Quemadas
        tempCode += metodoPrint
        tempCode += metodoPow
        tempCode += metodoPowString
        tempCode += metodoMod
        tempCode = tempCode + '\nfunc main(){\n'        
        tempCode = tempCode + "\n".join(self.code)
        tempCode = tempCode + '\n}\n'
        
        return tempCode
    

    #Generar un nuevo temporal
    def newTemp(self) -> str:
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        #Lo guardamos para declararlo
        self.tempList.append(temp)
        return temp

    #Generador de label
    def newLabel(self) -> str:
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)

    def addCallFunc(self, name: str):
        self.code.append(name + "();")

    #Añade label al codigo
    def addLabel(self, label: str):
        self.code.append(label + ":")

    def addExpression(self, target: str, left: str, right: str, operator: str):
        self.code.append(target + " = " + left + " " + operator + " " + right + ";")

    def addIf(self, left: str, rigth: str, operator: str, label: str):
        self.code.append("if " + left + " " + operator + " " + rigth + " {goto " + label + ";}")

    def addGoto(self, label:str):
        self.code.append("goto " + label + ";")

    #Añade un printf
    def addPrintf(self, typePrint:str, value:str):
        self.code.append("fmt.Printf(\"%" + typePrint + "\"," + value + ");")

    #Salto de linea
    def addNewLine(self):
        self.code.append('fmt.Printf(\"%c\",10);')

    #Se mueve hacia la posicion siguiente del heap
    def addNextHeap(self):
            self.code.append("H = H + 1;")
            self.H=self.H+1
    
    #Se mueve hacia la posicion siguiente del stack
    def addNextStack(self,index:str):
        self.code.append("P = P + " + str(index) + ";")
        self.P=self.P+index
      
    

    #Se mueve hacia la posicion anterior del stack
    def addBackStack(self, index:str):
            self.code.append("P = P - " + str(index) + ";")
            self.P=self.P-index

    #Obtiene el valor del heap en cierta posicion
    def addGetHeap(self, target:str, index: str):
        self.code.append(target + " = heap[int(" + index + ") ];")

    #Inserta valor en el heap
    def addSetHeap(self, index:str, value:str):
        self.code.append("heap[int(" + index + ")] = " + value + ";" )
    

    #Obtiene valor del stack en cierta posicion
    def addGetStack(self,target:str, index:str):
        self.code.append(target + " = stack[int(" + index + ")];")

    #INserta valor al stack
    def addSetStack(self, index:str, value:str):
        self.code.append("stack[int(" + index + ")] = " + value + ";" )
    
    def PointerFree(self, Indice):   
          
        sizeList= len(Listas.getListaSimbolo())
        if sizeList!=0:
            
            for position in Listas.getListaSimbolo():
                if str(Indice)==position[5]:
                    Indice=Indice+1 
                    self.PointerFree(Indice)
            
            return Indice
        
        return Indice