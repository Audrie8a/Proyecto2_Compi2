from datetime import datetime



class Listas:
    lstError=[]
    lstSalida=[]
    lstSimbolos=[]
    TablaSimbolos=[]
    lstOptimizados=[]
    idLst=[]
    lstAst=[]


    lstFunciones=[]
    FunctionActiva=False

    tempList=[]
    P=0
    H=0
    label=0
    temporal=0

    Errores=False
    Ast=False
    txtSalida=""

    #--------Banderas----------------
    cicloWhile=False
    cicloFor=False
    function=0
    
    retornar=False
    continuar=False
    romper=False


    @staticmethod
    def saveError(Descripcion, linea, columna):
        now = datetime.now()
        Fecha = now.strftime("%d/%m/%Y %H:%M:%S")
        Listas.lstError.append([len(Listas.lstError)+1,Descripcion,linea,columna,Fecha])
        

    @staticmethod
    def saveTabla(Nombre, Tipo, Ambito, visibilidad,tama,posicion, rol):
        now = datetime.now()
        Fecha = now.strftime("%d/%m/%Y %H:%M:%S")
        Listas.TablaSimbolos.append([Nombre,Tipo,Ambito,visibilidad,tama, posicion,rol, Fecha])
        contador=0
        for dato in Listas.lstSimbolos:
            if dato[0]==Nombre and dato[6]==rol and dato[2]==Ambito and dato[3]==visibilidad:
                Listas.lstSimbolos[contador]=[Nombre,Tipo,Ambito,visibilidad,tama,posicion,rol]  
                return;          
            contador=contador+1
        Listas.lstSimbolos.append([Nombre,Tipo,Ambito,visibilidad,tama, posicion,rol])
        Listas.guardarId(Nombre,rol)



    # False: Si existe, True: Si no existe puede crearlo
    @staticmethod
    def checkExistencia(Nombre, Tipo, Ambito, visibilidad,tama, rol):
        contador=0
        for dato in Listas.lstSimbolos:
            if dato[0]==Nombre and dato[6]!=rol:
                Listas.saveError("Error, ya se ha declarado otro dato con este id"+Nombre,0,0)
                print("Error, ya se ha declarado otro dato con este id"+Nombre)
                return False
            if dato[0]==Nombre and dato[6]==rol:
                return False
            contador=contador+1
        return True

    

    @staticmethod
    def searchTabla(Nombre, Ambito):
        for dato in Listas.lstSimbolos:
            if dato[0]==Nombre and dato[2]==Ambito:
                return dato
            
        return "empty"

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
        print("Nombre ", "Tipo ", "Ambito ", "Visibi ","Tama ", "Pos ", "Rol")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstSimbolos:
            print(var[0],var[1],var[2],var[3],var[4],var[5],var[6])

    def printTablaSimbolos():
        print("-----------------------------------------------------------------------------")
        print("---------------------------Tabla Simbolos------------------------------------")
        print("-----------------------------------------------------------------------------")
        print("Nombre ", "Tipo ", "Ambito ", "Visibi ","Tama ", "Pos ", "Rol ", "Hora")
        print("-----------------------------------------------------------------------------")
        for var in Listas.TablaSimbolos:
            print(var[0],var[1],var[2],var[3],var[4],var[5],var[6], var[7])

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
    
    def getOptimizado():
        return Listas.lstOptimizados

    def getAst():
        return Listas.lstAst

    def printAst():
        print("-----------------------------------------------------------------------")
        print("-------------------------------AST-------------------------------------")
        print("-----------------------------------------------------------------------")
        for var in Listas.lstAst:
            print(var)

    def guardarId(id,rol):
        condicion=True
        for ids in Listas.idLst:
            if ids==id :
                condicion=False
            
        if rol!="variable" and rol!="parameter":
            condicion=False

        if condicion:
            Listas.idLst.append(id)