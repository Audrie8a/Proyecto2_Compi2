from typing import List
from Impresiones3D.Impresiones import Impresiones
from Environment.Listas import Listas
class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.tamaStack=30101999
        self.resultado=[]

    #Obtener los temporales usados
    def getUsedTemps(self) -> str:
        return ",".join(Listas.tempList)
    
    def getUsedId(self) -> str:
        return ",".join(Listas.idLst)

    #Obtener el codigo generado
    def getCode(self) -> str:
        metodoPow=Impresiones.PotenciaAux
        metodoPrint=Impresiones.PrintAux
        metodoPowString=Impresiones.PotenciaStrAux
        metodoMod=Impresiones.ModAux
        metodoMenor=Impresiones.MenorAux
        metodoMayor=Impresiones.MayorAux
        metodoMenorQue=Impresiones.MenorQueAux
        metodoMayorQue=Impresiones.MayorQueAux
        metodoIgualIgual=Impresiones.IgualIgualAux
        metodoNoIgual=Impresiones.NoIgualAux
        metodoPrintBools=Impresiones.printBooleansAux
        metodoMenorStr= Impresiones.MenorStrAux
        metodoMayorStr= Impresiones.MayorStrAux
        metodoMenorQueStr= Impresiones.MenorQueStrAux
        metodoMayorQueStr= Impresiones.MayorQueStrAux
        metodoIgualIgualStr= Impresiones.IgualIgualStrAux
        metodoNoIgualStr= Impresiones.NoIgualStrAux
        metodoAndF= Impresiones.AndAux
        metodoOrF= Impresiones.OrAux
        metodoNotF= Impresiones.NotAux

       
        tempCode: str = 'package main;\n'
        tempCode = tempCode + 'import("fmt");\n'
        tempCode = tempCode + "\nvar P, H float64;\n"
        tempCode = tempCode + "var stack[78000]float64;\n"
        tempCode = tempCode + "var heap["+str(Listas.H)+"]float64;\n"


        if(len(Listas.tempList) > 0):
            tempCode = tempCode + "\nvar " + self.getUsedTemps() + " float64;\n"
        if(len(Listas.idLst)>0):
            tempCode = tempCode + "var " + self.getUsedId()+ " float64;\n"
        #Funciones Quemadas
        tempCode += metodoPrint
        tempCode += metodoPrintBools
        tempCode += metodoPow
        tempCode += metodoPowString
        tempCode += metodoMod
        tempCode += metodoMenor
        tempCode += metodoMayor
        tempCode += metodoMenorQue
        tempCode += metodoMayorQue
        tempCode += metodoIgualIgual
        tempCode += metodoNoIgual
        tempCode += metodoMenorStr
        tempCode += metodoMayorStr
        tempCode += metodoMenorQueStr
        tempCode += metodoMayorQueStr
        tempCode += metodoIgualIgualStr
        tempCode += metodoNoIgualStr
        tempCode += metodoAndF
        tempCode += metodoOrF
        tempCode += metodoNotF

 

        for symb in Listas.lstSimbolos:
            if symb[6]=="function":
                for fun in Listas.lstFunciones:
                    if fun[0]==symb[0] and fun[1]==symb[2]:
                        tempCode= tempCode+fun[2]
                        break

        tempCode = tempCode + '\nfunc main(){\n'    
        tempCode = tempCode + "\n".join(Listas.lstSalida)        
        tempCode = tempCode + "\n fmt.Printf(\"%c\",10);"
        tempCode = tempCode + '\n}\n'
        
        #print(tempCode)
        return tempCode
    

    #Generar un nuevo temporal
    def newTemp(self) -> str:
        temp = "t" + str(Listas.temporal)
        Listas.temporal = Listas.temporal + 1

        #Lo guardamos para declararlo
        for t in Listas.tempList:
            if temp==t:
                newT=self.newTemp()
                return newT
        Listas.tempList.append(temp)
        return temp

    #Generador de label
    def newLabel(self) -> str:
        temp = Listas.label
        Listas.label = Listas.label + 1
        return "L" + str(temp)

    def addCallFunc(self, name: str):
        self.saveCode(name + "();")

    #Añade label al codigo
    def addLabel(self, label: str):
        self.saveCode(label + ":")

    def addExpression(self, target: str, left: str, right: str, operator: str):
        self.saveCode(target + " = " + left + " " + operator + " " + right + ";")

    def addIf(self, left: str, rigth: str, operator: str, label: str):
        self.saveCode("if " + left + " " + operator + " " + rigth + " {goto " + label + ";}")

    def addGoto(self, label:str):
        self.saveCode("goto " + label + ";")

    #Añade un printf
    def addPrintf(self, typePrint:str, value:str):
        self.saveCode("fmt.Printf(\"%" + typePrint + "\"," + value + ");")

    #Salto de linea
    def addNewLine(self):
        self.saveCode('fmt.Printf(\"%c\",10);')

    #Se mueve hacia la posicion siguiente del heap
    def addNextHeap(self):
            self.saveCode("H = H + 1;")
            Listas.H=Listas.H+1
    
    #Se mueve hacia la posicion siguiente del stack
    def addNextStack(self,index:str):
        self.saveCode("P = P + " + str(index) + ";")
        Listas.P=Listas.P+index
      
    

    #Se mueve hacia la posicion anterior del stack
    def addBackStack(self, index:str):
            self.saveCode("P = P - " + str(index) + ";")
            Listas.P=Listas.P-index

    #Obtiene el valor del heap en cierta posicion
    def addGetHeap(self, target:str, index: str):
        self.saveCode(target + " = heap[int(" + index + ") ];")

    #Inserta valor en el heap
    def addSetHeap(self, index:str, value:str):
        self.saveCode("heap[int(" + index + ")] = " + value + ";" )
    

    #Obtiene valor del stack en cierta posicion
    def addGetStack(self,target:str, index:str):
        self.saveCode(target + " = stack[int(" + index + ")];")

    #INserta valor al stack
    def addSetStack(self, index:str, value:str):
        self.saveCode("stack[int(" + index + ")] = " + value + ";" )
    
    def PointerFree(self, Indice):   
          
        sizeList= len(Listas.getListaSimbolo())
        if sizeList!=0:
            
            for position in Listas.getListaSimbolo():
                if str(Indice)==position[5]:
                    Indice=Indice+1 
                    self.PointerFree(Indice)
            
            return Indice
        
        return Indice

    def saveCode(self,code):
        if Listas.FunctionActiva==False:
            Listas.lstSalida.append(code)
        else:
            Fin=len(Listas.lstFunciones)
            Listas.lstFunciones[Fin-1][2]=(Listas.lstFunciones[Fin-1][2]+code+"\n")

    
