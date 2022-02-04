from datetime import datetime
from typing import List

class Listas:
    lstError=[]
    lstSalida=[]
    lstSimbolos=[]
    lstAst=[]
    Errores=False
    Ast=False

    #--------Banderas----------------
    cicloWhile=False
    cicloFor=False
    function=False
    
    retornar=False
    continuar=False
    romper=False


    @staticmethod
    def saveError(Descripcion, linea, columna):
        now = datetime.now()
        Fecha = now.strftime("%d/%m/%Y %H:%M:%S")
        Listas.lstError.append([len(Listas.lstError)+1,Descripcion,linea,columna,Fecha])

    @staticmethod
    def saveTabla(Nombre, Tipo, Ambito, linea, columna):
        Listas.lstSimbolos.append([Nombre,Tipo,Ambito,linea,columna])

    @staticmethod
    def saveSalida(Entrada, tipoSalida):
        Listas.lstSalida.append([Entrada,tipoSalida])

    @staticmethod
    def saveAst(Entrada):
        Listas.lstAst.append(Entrada)

    def printErrores():
        print("-----------------------------------------------------------------------")
        print("---------------------------ERRORES-------------------------------------")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstError:
            print(var[0],var[1],var[2],var[3],var[4])
    
    def printSimbolos():
        print("-----------------------------------------------------------------------")
        print("---------------------------Simbolos------------------------------------")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstSimbolos:
            print(var[0],var[1],var[2],var[3],var[4])

    def printSaida():
        print("-----------------------------------------------------------------------")
        print("---------------------------Salida--------------------------------------")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstSalida:
            if (var[1]=='print'):
                print(var[0], end=" ")
            else:
                print(var[0])
    def getListSaida():
        return Listas.lstSalida
    
    def getListError():
        return Listas.lstError
    
    def getListaSimbolo():
        return Listas.lstSimbolos
        
    def setStautsError():
        if len(Listas.lstError)!= 0:
            Listas.Errores=True

    def LimpiarLsts():
        Listas.lstSalida.clear()
        Listas.lstError.clear()
        Listas.lstSimbolos.clear()
        Listas.lstAst.clear()

    def setErrores(valor):
        Listas.Errores=valor
    
    def getErrores():
        return Listas.Errores

    def getAst():
        return Listas.lstAst

    def printAst():
        print("-----------------------------------------------------------------------")
        print("-------------------------------AST-------------------------------------")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstAst:
            print(var)
