from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol
from Environment.Listas import Listas

class Environment:
    
    def __init__(self, father,nombre):
        #Usamos un diccionario para nuestra tabla de simbolos, guardara el id como clave y como cuerpo un simbolo
        self.variable = {}
        self.function={}
        self.Global={}
        self.Parameter={}
        self.Struct={}
        self.arreglos={}
        self.instancias=[]
        self.nombre=nombre
        
        #Father es el entorno exterior al cual podemos acceder
        self.father = father

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
                    if aux.getExtens()=='global': #Si la última declarada es global Edita
                        return aux
                    return None
                temp=temp.father
                
        elif Tipo==4: # Verifica si existe alguna variable con este id
            temp=self
            while (temp.father!=None):
                if(temp.variable.get(id)!=None):
                    aux = temp.variable.get(id)
                    if aux.getExtens()=='local': #Si la última declarada es global Edita
                        return aux
                    return None
                temp=temp.father
        return None
    
    def saveVariable(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        try:
            if self.father==None:
                self.saveVariableGlobal(id,value,type,isArray,linea,columna)
            else:                
                if (self.VerificarExistencias(id,3)!=None  ): #Ya está declarada global
                    value=Symbol(id,value,type,'global',linea,columna)
                    self.alterVariable(id,'global',value,linea,columna)
                elif (self.VerificarExistencias(id,4)!=None):
                    value=Symbol(id,value,type,'local',linea,columna)
                    self.alterVariable(id,'local',value,linea,columna)
                else:
                    self.saveVariableLocal(id,value,type,isArray,linea,columna)
                    


        except:
            print("Error al manejar Variable " + id ,linea,columna)
            Listas.saveError("Error al manejar Variable " + id,linea,columna)
            return None

    def saveParameter(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        
        try:
            if (self.Parameter.get(id) != None):
                print("Parametro " + id + " Está repetido!")
                Listas.saveError("Parametro " + id + " Está repetido!",linea,columna)
                return
            tempVar = Symbol(id,value,type,"Parameter",linea,columna)
            tempVar.array = isArray
            self.Parameter[id] = tempVar
            Listas.saveTabla(id,'Parameter',self.nombre,linea,columna)
        except:            
            print("Error al crear Variable " + id ,linea,columna)
            Listas.saveError("Error al crear Variable " + id,linea,columna)
            return None

    def saveVariableLocal(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        try:
            if self.father==None:            
               return None 
            elif self.Parameter.get(id)!=None:
                print("Error al crear Variable, Parametro existente con este id: " + id ,linea,columna)
                Listas.saveError("Error al crear Variable, Parametro existente con este id: " + id,linea,columna)
                return None
            else:
                if (self.VerificarExistencias(id,1)!=None):
                    print("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!",linea,columna)
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!",linea,columna)
                    return None
                tempVar = Symbol(id,value,type,"local",linea,columna)
                tempVar.array = isArray
                self.variable[id] = tempVar
                Listas.saveTabla(id,'variable','local',linea,columna)
        except:
            print("Error al crear Variable " + id ,linea,columna)
            Listas.saveError("Error al crear Variable " + id,linea,columna)
            return None

    def saveVariableGlobal(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        try:
            existencia=self.VerificarExistencias(id,3)
            if self.father!=None: # Si estamos fuera del entorno global
                if (existencia!=None): #Si existe una global declarada a lo último se edita
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,value,type,'global',linea,columna)
                        self.alterVariable(id,'global',value,linea,columna)
                elif (self.VerificarExistencias(id,2)!=None): #Si existe alguna estructura con este id
                    print("Error, ya se ha declarado una dato con este id. La variable global " + id + " no se pudo guradar!",linea,columna)
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable global" + id + " no se pudo guradar!",linea,columna)
                    return
                else:   #Si ninguna de las anteriores cumple, se puede declarar
                    tempVar = Symbol(id,value,type,"global",linea, columna)
                    tempVar.array = isArray
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,'variable','global',linea,columna)
            else:
                aux=self.variable.get(id)
                if aux==None :
                    tempVar = Symbol(id,value,type,"global",linea, columna)
                    tempVar.array = isArray
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,'variable','global',linea,columna)
                elif aux!=None and aux.extens=='global':
                    if type!= typeExpression.OBJETO: #Si existe, pero solo se está mandando a llamar se omite
                        value=Symbol(id,value,type,'global',linea,columna)
                        self.alterVariable(id,'global',value,linea,columna)
        except:
            print("Error al crear Variable " + id ,linea,columna)
            Listas.saveError("Error al crear Variable " + id,linea,columna)
            return None

    def getVariable(self, id: str,linea,columna) -> Symbol:
        try:
            if self.Parameter.get(id)==None:
                
                condicion=0
                tempEnv = self
                tempEnvGlobal = self
                tempArr=self
                
                while(tempEnv != None):
                    if(tempEnv.variable.get(id) != None):
                        if tempEnv.variable.get(id).getType()!=typeExpression.OBJETO:
                            if(tempEnv.variable.get(id).getExtens()=='local' and condicion!=0):
                                print("Error: la variable " + id + " no existe")                      
                                Listas.saveError("Error: la variable" + id + " no existe" + id,linea,columna)
                                return None
                            else:
                                return tempEnv.variable.get(id).getValue()
                        else:
                            print("\n Error, la variable "+id+". Valor indefinido!")
                            Listas.saveError("Error, la variable"+id+". Valor indefinido!")
                        
                    tempEnv = tempEnv.father
                    condicion=condicion+1                                  
                       
                
                
                
                while(tempEnvGlobal != None):
                    if(tempEnvGlobal.Global.get(id) != None):
                        if tempEnvGlobal.Global.get(id).getType()!=typeExpression.OBJETO:
                            return tempEnvGlobal.Global.get(id).getValue()
                        else:
                            print("Error: la variable " + id + " no existe")                      
                            Listas.saveError("Error: la variable " + id + " no existe" + id,linea,columna)
                            return None
                    tempEnvGlobal = tempEnvGlobal.father
                    
                    
                while(tempArr!=None):
                    if(tempArr.arreglos.get(id)!=None):
                        return tempArr.arreglos.get(id).lstVal
                    tempArr=tempArr.father
               
                print("\n Error, la variable "+id+". Valor indefinido!")
                Listas.saveError("Error, la variable"+id+". Valor indefinido!")
            else:
            
                tempEnv = self
                
                while(tempEnv != None):
                    if(tempEnv.Parameter.get(id) != None):
                        return tempEnv.Parameter.get(id).getValue()                        
                    else:
                        print("Error: el parámetro " + id + " no existe")                      
                        Listas.saveError("Error: el parámetro " + id + " no existe" + id,linea,columna)
                        return None                        
                    tempEnv = tempEnv.father
        except:
            print("Error al obtener Variable " + id ,linea,columna)
            Listas.saveError("Error al obtener Variable " + id,linea,columna)
            return None

    def alterParametro(self, id: str, value: Symbol,linea,columna):
        try:
            tempEnv = self
            if(tempEnv.Parameter.get(id) != None):
                tempVar: Symbol = tempEnv.Parameter.get(id)
                tempVar.value = value.getValue()
                self.Parameter[id] = tempVar
                return
            print("Error: el Parametro " + id + " no existe",linea,columna)            
            Listas.saveError("Error: el Parametro " + id + " no existe",linea,columna)
            return None
        except:            
            print("Error al eidtar Parametro " + id ,linea,columna)
            Listas.saveError("Error al eidtar Parametro " + id,linea,columna)
            return None

    def alterVariable(self, id: str,tipo, value: Symbol,linea,columna):
        try:
            tempEnv = self
            while(tempEnv != None):
                if(tempEnv.variable.get(id) != None and tempEnv.variable.get(id).extens==tipo):
                    tempVar: Symbol = tempEnv.variable.get(id)
                    if tempVar.type==typeExpression.OBJETO:
                        tempVar.type=value.getType()
                    tempVar.value = value.getValue()
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,'variable',tipo,linea,columna)
                    return
                tempEnv = tempEnv.father
            print("Error: la variable " + id + " no existe",linea,columna)
            Listas.saveError("Error: la variable " + id + " no existe" + id,linea,columna)
            return None
        except:
            print("Error al asignar valor variable " + id ,linea,columna)
            Listas.saveError("Error al asignar valor variable " + id,linea,columna)
            return None

    def alterVariableGlobal(self, id: str, value: Symbol,linea,columna):
        try:
            tempEnv = self
            while(tempEnv != None):
                if(tempEnv.Global.get(id) != None):
                    tempVar: Symbol = tempEnv.Global.get(id)
                    if tempVar.type==typeExpression.OBJETO:
                        tempVar.type=value.getType()
                    tempVar.value = value.getValue()
                    self.Global[id] = tempVar
                    Listas.saveTabla(id,'variable','global',linea,columna)
                    return
                tempEnv = tempEnv.father
            print("Error: la variable " + id + " no existe",linea,columna)
            Listas.saveError("Error: la variable " + id + " no existe" + id,linea,columna)
            return None
        except:
            print("Error al asignar valor variable " + id ,linea,columna)
            Listas.saveError("Error al asignar valor variable " + id,linea,columna)
            return None

    def saveFunction(self, id: str, function,linea,columna):
        try:
            globalEntorno=self.getGlobal().Global
            if (self.function.get(id) != None or self.variable.get(id)!=None or globalEntorno.get(id)!=None or self.Struct.get(id)!=None or self.arreglos.get(id)!=None or self.verificarConstructor(id)==True):
                print("Error, ya se ha declarado una dato con este id. La funcion " + id + " no se pudo guradar!",linea,columna)
                Listas.saveError("Error, ya se ha declarado una dato con este id. La funcion " + id + " no se pudo guradar!",linea,columna)
                return
            self.function[id] = function
            Listas.saveTabla(id,'funcion',self.nombre,linea,columna)
        except:
            print("Error al salvar la función " + id ,linea,columna)
            Listas.saveError("Error al salvar la función " + id,linea,columna)
    
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

    def instanceStruct(self,Struct,variable,tipo,parametros,id,linea,columna):
        tempVar: Struct =self.Struct.get(id)
        try:
            if(tempVar!=None):
                self.instancias.append([tempVar.id,variable,tipo,parametros])                
        except:
            print("Error al generar constructor " + id ,linea,columna)
            Listas.saveError("Error al generar constructor" + id,linea,columna)
            return None

    def verificarConstructor(self,id):
        tempEnv=self
        while(tempEnv != None):
            for ins in tempEnv.instancias:
                if(ins[1]==id):
                    return True
                    
            tempEnv = tempEnv.father
        
        return False

    def getValorStruct(self,id, atributo,linea,columna):
        tempEnv=self
        while(tempEnv != None):
            for ins in tempEnv.instancias:
                if(ins[1]==id):
                    
                    aux= tempEnv.Struct.get(ins[0])
                    if aux!=None:
                        contador=0
                        valor=any
                        
                        for atb in aux.blockAtributos:
                            temporal = ins[3][contador].execute(self)    
                            if atb.id==atributo:
                                valor=temporal.getValue()
                                tipo = temporal.getType()
                                return Symbol("",valor,tipo,ins[2],linea,columna)
                            contador=contador+1


                   

            tempEnv=tempEnv.father
        print("No se logró obtener el valor de "+id+"."+atributo)
        Listas.saveError("No se logró obtener el valor de "+id+"."+atributo,linea,columna)
        return Symbol("",None,typeExpression.STRING,"",linea,columna)

    
    def alterValorStruct(self,id,atributo,valorNuevo,tipoValorNuevo,linea,columna):
        tempEnv=self
        while(tempEnv != None):
            contadorInst=0
            for ins in tempEnv.instancias:
                if(ins[1]==id):
                    
                    aux= tempEnv.Struct.get(ins[0])
                    if aux!=None:
                        if aux.tipoStruct!=None:
                            contador=0
                            valor=any
                            
                            for atb in aux.blockAtributos:  
                                if atb.id==atributo:
                                    if atb.type==tipoValorNuevo and atb.type!=typeExpression.OBJETO:
                                        temporal=ins
                                        temporal[3][contador].value=valorNuevo
                                        temporal[3][contador].type=tipoValorNuevo
                                    
                                    tempEnv.instancias[contadorInst]=temporal
                                    return
                                contador=contador+1
                        else:
                            print("No se permite modificar este struct! "+id+"."+atributo)
                            Listas.saveError("No se permite modificar este struct! "+id+"."+atributo,linea,columna)
                            return Symbol("",None,typeExpression.STRING,"",linea,columna)
                    

            tempEnv=tempEnv.father
            contadorInst=contadorInst+1
        
        print("No se logró modificar el valor de "+id+"."+atributo)
        Listas.saveError("No se logró modificar el valor de "+id+"."+atributo,linea,columna)
        return Symbol("",None,typeExpression.STRING,"",linea,columna)

    def saveArreglo(self,id,arreglo,linea,columna):
        try:
            globalEntorno=self.getGlobal()
            if (self.Struct.get(id) != None or self.verificarConstructor(id)==True):
                print("No se puede crear arreglo, ya existe un dato con la identificacion " + id ,linea,columna)
                Listas.saveError("No se puede crear arreglo, ya existe un dato con la identificacion " + id ,linea,columna)
                return
            elif(self.variable.get(id) != None or globalEntorno.Global.get(id)!=None ):
                print("Error al crear arreglo, Ya se encuentra una variable con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra una variable con esta identificación:  " + id ,linea,columna)
                return
            elif (self.function.get(id) != None):
                print("Error al crear arreglo, Ya se encuentra una función con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra una función con esta identificación:  " + id ,linea,columna)
                return
            elif (self.arreglos.get(id) != None):
                print("Error al crear arreglo, Ya se encuentra un arreglo con esta identificación: " + id ,linea,columna)
                Listas.saveError("Error al crear Struct, Ya se encuentra un arreglo con esta identificación:  " + id ,linea,columna)
                return
            self.arreglos[id] = arreglo
            Listas.saveTabla(id,'arreglo',arreglo.type,linea,columna)
        except:
            print("Error al salvar la struct " + id ,linea,columna)
            Listas.saveError("Error al salvar la struct " + id,linea,columna)
           
    
    def getArreglo(self, id: str,arreglo,linea,columna) -> Symbol:
        try:
            tempEnv = self                
            while(tempEnv != None):
                if(tempEnv.arreglos.get(id) != None):
                    temporal =tempEnv.arreglos.get(id)
                    aux=temporal.lstVal
                    for ins in arreglo.lstVal:
                        aux=aux[ins.getValue()-1]

                    return aux    
                        
                tempEnv = tempEnv.father                
                
        except:
            print("Error al obtener valor Arreglo " + id ,linea,columna)
            Listas.saveError("Error al obtener valor Arreglo " + id,linea,columna)
            return None

    def getLengthArreglo(self, id: str,linea,columna) -> Symbol:
        try:
            tempEnv = self                
            while(tempEnv != None):
                if(tempEnv.arreglos.get(id) != None):
                    temporal =tempEnv.arreglos.get(id)
                    return Symbol("",len(temporal.lstVal),typeExpression.INTEGER,"",linea,columna)
                        
                tempEnv = tempEnv.father                
                
        except:
            print("Error al obtener length Arreglo " + id ,linea,columna)
            Listas.saveError("Error al obtener length Arreglo " + id,linea,columna)
            return None