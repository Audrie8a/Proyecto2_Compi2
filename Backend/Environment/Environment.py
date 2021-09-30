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

    
    def saveVariable(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        try:
            if self.Parameter.get(id)==None:

                if (self.variable.get(id) != None): #Encontro una local la edita
                    self.alterVariable(id,Symbol(id,value,type,self.variable.get(id).getExtens(),self.variable.get(id).getLine(),self.variable.get(id).getColumn()),linea,columna)
                else: #Busca una Global
                    tempEnvGlobal = self
                    tempEnv = self

                    condicion=False
                    while(tempEnvGlobal != None):
                        if(tempEnvGlobal.Global.get(id) != None):
                            condicion=True
                            break
                        tempEnvGlobal = tempEnvGlobal.father

                    if condicion: # Si es una global creo una nueva variable
                        if self.function.get(id)!=None or self.Struct.get(id)!=None or self.verificarConstructor(id)==True:
                            print("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                            Listas.saveError("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                            return
                        
                        tempVar = Symbol(id,value,type,"none",linea,columna)
                        tempVar.array = isArray
                        self.variable[id] = tempVar
                        Listas.saveTabla(id,'variable','none',linea,columna)
                    else:
                        while(tempEnv != None):
                            if(tempEnv.variable.get(id) != None):                        
                                break
                            tempEnv = tempEnv.father
                        if tempEnv!= None:
                            if tempEnv.variable.get(id)!=None:
                                if tempEnv.variable.get(id).getExtens()=='none':
                                    self.alterVariable(id,Symbol(id,value,type,tempEnv.variable.get(id).getExtens(),tempEnv.variable.get(id).getLine(),tempEnv.variable.get(id).getColumn()),linea,columna)
                                else:
                                    if self.function.get(id)!=None  or self.Struct.get(id)!=None or self.verificarConstructor(id)==True:
                                        print("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                        Listas.saveError("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                        return
                                    tempVar = Symbol(id,value,type,"none",linea,columna)
                                    tempVar.array = isArray
                                    self.variable[id] = tempVar
                                    Listas.saveTabla(id,'variable','none',linea,columna)
                            else:
                                if self.function.get(id)!=None  or self.Struct.get(id)!=None or self.verificarConstructor(id)==True:
                                    print("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                    return
                                tempVar = Symbol(id,value,type,"none",linea,columna)
                                tempVar.array = isArray
                                self.variable[id] = tempVar

                                Listas.saveTabla(id,'variable','none',linea,columna)
                        else:
                            if self.function.get(id)!=None  or self.Struct.get(id)!=None or self.verificarConstructor(id)==True:
                                print("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                Listas.saveError("Error, ya se ha declarado una dato con este id. La variable " + id + " no se pudo guradar!",linea,columna)
                                return

                            tempVar = Symbol(id,value,type,"none",linea,columna)
                            tempVar.array = isArray
                            self.variable[id] = tempVar 
                            Listas.saveTabla(id,'variable','none',linea,columna)
            else:
                self.alterVariable(id,Symbol(id,value,type,self.Parameter.get(id).getExtens(),self.Parameter.get(id).getLine(),self.Parameter.get(id).getColumn()),linea,columna)
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
            if self.Parameter.get(id)==None:
                
                if (self.variable.get(id) != None or self.verificarConstructor(id)==True or self.Global.get(id) != None or self.function.get(id)!=None or self.Struct.get(id)!=None or self.arreglos.get(id)!=None):
                    print("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!",linea,columna)
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable local " + id + " no se pudo guradar!",linea,columna)
                    return None
                tempVar = Symbol(id,value,type,"local",linea,columna)
                tempVar.array = isArray
                self.variable[id] = tempVar
                Listas.saveTabla(id,'variable','local',linea,columna)
            else:
                print("Error al crear Variable "+id+". Se encuentra un parámetro con este Id")               
                Listas.saveError("Error al crear Variable "+id+". Se encuentra un parámetro con este Id",linea,columna)
        except:
            print("Error al crear Variable " + id ,linea,columna)
            Listas.saveError("Error al crear Variable " + id,linea,columna)
            return None

    def saveVariableGlobal(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        try:
            if self.Parameter.get(id)==None:
                if (self.Global.get(id) != None and (self.function.get(id) == None or self.Struct.get(id)==None )):
                    self.alterVariableGlobal(id,Symbol(id,value,type,self.getGlobal().Global.get(id).getExtens(),self.getGlobal().Global.get(id).getLine(),self.getGlobal().Global.get(id).getColumn()),linea,columna)
                    return None
                elif self.function.get(id) != None  or self.Struct.get(id)!=None:
                    print("Error, ya se ha declarado una dato con este id. La variable global " + id + " no se pudo guradar!",linea,columna)
                    Listas.saveError("Error, ya se ha declarado una dato con este id. La variable global" + id + " no se pudo guradar!",linea,columna)
                    return
                tempVar = Symbol(id,value,type,"global",linea, columna)
                tempVar.array = isArray
                self.Global[id] = tempVar
                Listas.saveTabla(id,'variable','global',linea,columna)
            else:
                print("Error al crear Variable "+id+". Se encuentra un parámetro con este Id")
                Listas.saveError("Error al crear Variable "+id+". Se encuentra un parámetro con este Id",linea,columna)
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

    def alterVariable(self, id: str, value: Symbol,linea,columna):
        try:
            tempEnv = self
            while(tempEnv != None):
                if(tempEnv.variable.get(id) != None):
                    tempVar: Symbol = tempEnv.variable.get(id)
                    if tempVar.type==typeExpression.OBJETO:
                        tempVar.type=value.getType()
                    tempVar.value = value.getValue()
                    self.variable[id] = tempVar
                    Listas.saveTabla(id,'variable','',linea,columna)
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