from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Listas import Listas
from Impresiones3D.Impresiones import Impresiones

class Environment:

    def __init__(self, father,Nombre) -> None:
        self.father = father
        self.variable = {}
        self.Global={}
        self.function={}
        self.Parameter={}
        self.Struct={}
        self.arreglos={}
        self.instancias=[]
        self.size = 0
        self.Nombre=Nombre

        if(father != None):
            self.size = father.size



    def getGlobal(self):
        tempEnv: Environment = self;
        while(tempEnv.father != None):
            tempEnv = tempEnv.father
        return tempEnv

    def VerificarExistencias(self,id,Tipo):
        if Tipo==1: #Verifica para Nuevas Locales
            if (self.variable.get(id) != None 
                or self.verificarConstructor(id)==True 
                or self.function.get(id)!=None 
                or self.Struct.get(id)!=None 
                or self.arreglos.get(id)!=None):
                return True
        elif Tipo==2: #Verifica para nuevas Globales
            if ((self.variable.get(id) != None and self.variable.get(id)=='local')
                or self.verificarConstructor(id)==True
                or self.function.get(id)!=None 
                or self.Struct.get(id)!=None 
                or self.arreglos.get(id)!=None):
                return True
        elif Tipo==3: #Verifica existencia en Globales
            temp=self
            while (temp.father!=None):
                if(temp.variable.get(id)!=None):
                    aux = temp.variable.get(id)
                    if aux.getVisibilidad()=='global': #Si la última declarada es global Edita
                        return aux
                    return None
                temp=temp.father
                
        elif Tipo==4: # Verifica si existe alguna variable con este id
            temp=self
            while (temp.father!=None):
                if(temp.variable.get(id)!=None):
                    aux = temp.variable.get(id)
                    if aux.getVisibilidad()=='local': #Si la última declarada es global Edita
                        return aux
                    return None
                temp=temp.father
        return None

    def verificarConstructor(self,id):
        tempEnv=self
        while(tempEnv != None):
            for ins in tempEnv.instancias:
                if(ins[1]==id):
                    return True
                    
            tempEnv = tempEnv.father
        
        return False

    #id - tipo - ambito - visibilidad - tama - posición - rol
    #x    int    father   global        1      0          varaible
    def saveVariable(self, id: str,  type: typeExpression, tama,pos,value,rol):
        try:
            if self.father==None:
                return self.saveVariableGlobal(id,type,tama,pos,value,rol)
            else:                
                if (self.VerificarExistencias(id,3)!=None  ): #Ya está declarada global
                    value=Symbol(id, type,self.Nombre,'global',tama,pos,rol,value)
                    return self.alterVariable(id,'global',value)
                elif (self.VerificarExistencias(id,4)!=None):
                    value=Symbol(id,type,self.Nombre,'local',tama,pos,rol,value)
                    return self.alterVariable(id,'local',value)
                else:
                    return self.saveVariableLocal(id,type,tama,pos,value,rol)
        except:
            print("Error al manejar Variable " + id )
            Listas.saveError("Error al manejar Variable " + id,0,0)
            return None

    #id - tipo - ambito - visibilidad - tama - posición - rol
    #x    int    father   global        1      0          varaible
    def saveVariableLocal(self, id: str,  type: typeExpression, tama,pos,value,rol):
        try:
            if self.father==None:            
                print("Error al declarar Variable " + id )
                Listas.saveError("Error al declarar Variable " + id+". No se puede declarar una variable local en el entorno father ",0,0)
                return None
            elif self.Parameter.get(id)!=None:
                print("Error al crear Variable, Parametro existente con este id: " + id )
                Listas.saveError("Error al crear Variable, Parametro existente con este id: " + id,0,0)
                return None
            else:
                if (self.VerificarExistencias(id,1)!=None):
                    print("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!")
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!",0,0)
                    return None
                tempVar = Symbol(id,type,self.Nombre,"local",tama,pos,rol,value)
                self.variable[id] = tempVar
                Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,'local',tama,pos,rol)
                return tempVar
        except:
            print("Error al crear Variable " + id )
            Listas.saveError("Error al crear Variable " + id,0,0)
            return None

    def saveVariableGlobal(self, id: str,  type: typeExpression, tama,pos,value,rol):
        try:
            existencia=self.VerificarExistencias(id,3)
            if self.father!=None: # Si estamos fuera del entorno global
                if (existencia!=None): #Si existe una global declarada a lo último se edita
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,type,self.Nombre,'global',tama,pos,rol,value)
                        return self.alterVariable(id,'global',value)
                elif (self.VerificarExistencias(id,2)!=None): #Si existe alguna estructura con este id
                    print("Error, ya se ha declarado una dato con este id. La variable global " + id + " no se pudo guradar!")
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable global" + id + " no se pudo guradar!",0,0)
                    return
                else:   #Si ninguna de las anteriores cumple, se puede declarar
                    tempVar = Symbol(id,type,self.Nombre,"global",tama,value,rol,value)
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,"global",tama,pos,rol)
                    return tempVar
            else:
                aux=self.variable.get(id)
                if aux==None :
                    tempVar = Symbol(id,type,self.Nombre,"global",tama,pos,rol,value)
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,"global",tama,pos,rol)
                    return tempVar
                elif aux!=None and aux.Visibilidad=='global':
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,type,self.Nombre,'global',tama,pos,rol,value)
                        return self.alterVariable(id,'global',value)
        except:
            print("Error al crear Variable " + id )
            Listas.saveError("Error al crear Variable " + id,0,0)
            return None

    def alterVariable(self, id: str,tipo, value: Symbol):
        try:
            tempEnv = self
            while(tempEnv != None):
                if(tempEnv.variable.get(id) != None and tempEnv.variable.get(id).Visibilidad==tipo):
                    tempVar: Symbol = tempEnv.variable.get(id)
                    if tempVar.Tipo==typeExpression.OBJETO:
                        tempVar.Tipo=value.Tipo
                    tempVar.value = value.value
                    self.variable[id] = tempVar
                    datoTabla=Listas.searchTabla(id,value.Ambito)
                    Listas.saveTabla(id,self.convertTipoTabla(tempVar.Tipo),self.Nombre,tempVar.Visibilidad,tempVar.Tama,tempVar.Position,datoTabla[6])
                    return tempVar
                tempEnv = tempEnv.father
            print("Error: la variable " + id + " no existe")
            Listas.saveError("Error: la variable " + id + " no existe" + id,0,0)
            return None
        except:
            print("Error al asignar valor variable " + id )
            Listas.saveError("Error al asignar valor variable " + id,0,0)
            return None

    def getVariable(self, id: str) -> Symbol:
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                return tempEnv.variable.get(id)
            tempEnv = tempEnv.father
        print("Error: la variable " + id + " no existe")
        return None
    
    def convertTipoTabla(self,tipo):
        if tipo ==typeExpression.INTEGER:
            return "integer"
        elif tipo==typeExpression.STRING:
            return "string"
        elif tipo==typeExpression.BOOL:
            return "bool"
        elif tipo== typeExpression.CHAR:
            return "char"
        elif tipo==typeExpression.FLOAT:
            return "float"
        elif tipo==typeExpression.OBJETO:
            return "object"

    def saveParameter(self, id: str, value, type: typeExpression, pos, linea, columna):
        
        try:
            if (self.Parameter.get(id) != None):
                print("Parametro " + id + " Está repetido!")
                Listas.saveError("Parametro " + id + " Está repetido!",linea,columna)
                return
            tempVar = Symbol(id,type,self.Nombre,"local","1",pos,"parameter",value)
            self.Parameter[id] = tempVar
            Listas.saveTabla(id,type,self.Nombre,"local","1",pos,"parameter")
        except:            
            print("Error al crear Variable " + id ,linea,columna)
            Listas.saveError("Error al crear Variable " + id,linea,columna)
            return None
        
    
    def saveFunction(self, id: str, function,tama,linea,columna):
        try:
            globalEntorno=self.getGlobal().Global
            if (self.function.get(id) != None or self.variable.get(id)!=None or globalEntorno.get(id)!=None or self.Struct.get(id)!=None or self.arreglos.get(id)!=None or self.verificarConstructor(id)==True):
                print("Error, ya se ha declarado una dato con este id. La funcion " + id + " no se pudo guradar!",linea,columna)
                Listas.saveError("Error, ya se ha declarado una dato con este id. La funcion " + id + " no se pudo guradar!",linea,columna)
                return
            self.function[id] = function
            visi="global"
            if self.Nombre!="father":
                visi="local"
            Listas.saveTabla(id,"void",self.Nombre,visi,tama,"~","function")
        except:
            print("Error al salvar la función " + id ,linea,columna)
            Listas.saveError("Error al salvar la función " + id,linea,columna)

    def getFunction(self, id: str,linea,columna):
        try:
            tempEnv = self
            while(tempEnv != None):
                if(tempEnv.function.get(id) != None):
                    return ["Funcion",tempEnv.function.get(id)]
                elif tempEnv.Struct.get(id)!=None:
                    return ["Struct",tempEnv.Struct.get(id)]
                tempEnv = tempEnv.father
            print("Error: la función " + id + " no existe",linea,columna)
            Listas.saveError("Error: la función " + id + " no existe" + id,linea,columna)
            return None
        except:
            print("Error al buscar la función " + id ,linea,columna)
            Listas.saveError("Error al buscar la función " + id,linea,columna)
            return None

    def saveStruct(self,id,struct,linea,columna):
        try:
            globalEntorno=self.getGlobal()
            if (self.Struct.get(id) != None or self.verificarConstructor(id)==True):
                print("La estructura " + id + " ya existe",linea,columna)
                Listas.saveError("La estructura " + id + " ya existe",linea,columna)
                return
            elif(self.variable.get(id) != None or globalEntorno.Global.get(id)!=None ):
                print("Error al crear Struct, Ya se encuentra una variable con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra una variable con esta identificación:  " + id ,linea,columna)
                return
            elif (self.function.get(id) != None):
                print("Error al crear Struct, Ya se encuentra una función con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra una función con esta identificación:  " + id ,linea,columna)
                return
            elif (self.arreglos.get(id) != None):
                print("Error al crear Struct, Ya se encuentra un arreglo con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra un arreglo con esta identificación:  " + id ,linea,columna)
                return
            self.Struct[id] = struct
            Listas.saveTabla(id,'struct',struct.tipoStruct,linea,columna)
        except:
            print("Error al salvar la struct " + id ,linea,columna)
            Listas.saveError("Error al salvar la struct " + id,linea,columna)
    