from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Listas import Listas

class Environment:

    def __init__(self, father,Nombre) -> None:
        self.father = father
        self.variable = {}
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
    def saveVariable(self, id: str,  type: typeExpression, tama,pos,value):
        try:
            if self.father==None:
                return self.saveVariableGlobal(id,type,tama,pos,value)
            else:                
                if (self.VerificarExistencias(id,3)!=None  ): #Ya está declarada global
                    value=Symbol(id, type,self.Nombre,'global',tama,pos,'variable',value)
                    return self.alterVariable(id,'global',value)
                elif (self.VerificarExistencias(id,4)!=None):
                    value=Symbol(id,type,self.Nombre,'local',tama,pos,'variable',value)
                    return self.alterVariable(id,'local',value)
                else:
                    return self.saveVariableLocal(id,type,tama,pos,value)
        except:
            print("Error al manejar Variable " + id )
            Listas.saveError("Error al manejar Variable " + id,0,0)
            return None

    #id - tipo - ambito - visibilidad - tama - posición - rol
    #x    int    father   global        1      0          varaible
    def saveVariableLocal(self, id: str,  type: typeExpression, tama,pos,value):
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
                tempVar = Symbol(id,type,self.Nombre,"local",tama,pos,'variable',value)
                self.variable[id] = tempVar
                Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,'local',tama,pos,'variable')
                return tempVar
        except:
            print("Error al crear Variable " + id )
            Listas.saveError("Error al crear Variable " + id,0,0)
            return None

    def saveVariableGlobal(self, id: str,  type: typeExpression, tama,pos,value):
        try:
            existencia=self.VerificarExistencias(id,3)
            if self.father!=None: # Si estamos fuera del entorno global
                if (existencia!=None): #Si existe una global declarada a lo último se edita
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,type,self.Nombre,'global',tama,pos,'variable',value)
                        return self.alterVariable(id,'global',value)
                elif (self.VerificarExistencias(id,2)!=None): #Si existe alguna estructura con este id
                    print("Error, ya se ha declarado una dato con este id. La variable global " + id + " no se pudo guradar!")
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable global" + id + " no se pudo guradar!",0,0)
                    return
                else:   #Si ninguna de las anteriores cumple, se puede declarar
                    tempVar = Symbol(id,type,self.Nombre,"global",tama,value,'variable',value)
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,"global",tama,pos,'variable')
                    return tempVar
            else:
                aux=self.variable.get(id)
                if aux==None :
                    tempVar = Symbol(id,type,self.Nombre,"global",tama,pos,'variable',value)
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,self.convertTipoTabla(type),self.Nombre,"global",tama,pos,'variable')
                    return tempVar
                elif aux!=None and aux.Visibilidad=='global':
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,type,self.Nombre,'global',tama,pos,'variable',value)
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
                    Listas.saveTabla(id,self.convertTipoTabla(tempVar.Tipo),self.Nombre,tempVar.Visibilidad,tempVar.Tama,tempVar.Position,'variable')
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