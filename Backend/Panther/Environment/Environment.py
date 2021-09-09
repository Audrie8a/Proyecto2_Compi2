from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol

class Environment:
    
    def __init__(self, father):
        #Usamos un diccionario para nuestra tabla de simbolos, guardara el id como clave y como cuerpo un simbolo
        self.variable = {}
        self.function={}
        self.Global={}
        #Father es el entorno exterior al cual podemos acceder
        self.father = father

    def getGlobal(self):
        tempEnv: Environment = self;
        while(tempEnv.father != None):
            tempEnv = tempEnv.father
        return tempEnv

    def saveVariable(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        if (self.variable.get(id) != None): #Encontro una local la edita
            self.alterVariable(id,Symbol(id,value,type,self.variable.get(id).getExtens(),self.variable.get(id).getLine(),self.variable.get(id).getColumn()),linea,columna)
        else: #Busca una Global
            tempEnvGlobal = self
            condicion=False
            while(tempEnvGlobal != None):
                if(tempEnvGlobal.Global.get(id) != None):
                    condicion=True
                    break
                tempEnvGlobal = tempEnvGlobal.father

            if condicion:
                self.alterVariableGlobal(id,Symbol(id,value,type,tempEnvGlobal.Global.get(id).getExtens(),tempEnvGlobal.Global.get(id).getLine(),tempEnvGlobal.Global.get(id).getColumn()),linea,columna)
            else:
                tempVar = Symbol(id,value,type,"none",linea,columna)
                tempVar.array = isArray
                self.variable[id] = tempVar
    
    def saveVariableLocal(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        if (self.variable.get(id) != None or self.Global.get(id) != None):
            print("La variable " + id + " ya existe")
            return None
        tempVar = Symbol(id,value,type,"local",linea,columna)
        tempVar.array = isArray
        self.variable[id] = tempVar

    def saveVariableGlobal(self, id: str, value, type: typeExpression, isArray: bool, linea, columna):
        if (self.Global.get(id) != None):
            print("La variable " + id + " ya existe")
            return None
        tempVar = Symbol(id,value,type,"global",linea, columna)
        tempVar.array = isArray
        self.Global[id] = tempVar
    
    def getVariable(self, id: str,linea,columna) -> Symbol:
        condicion=0
        tempEnv = self
        tempEnvGlobal = self
         
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                if(tempEnv.variable.get(id).getExtens()=='local' and condicion!=0):
                    print("Error: la variable " + id + " no existe")
                    return None
                else:
                    return tempEnv.variable.get(id).getValue()
                    
            tempEnv = tempEnv.father
            condicion=condicion+1

        

        while(tempEnvGlobal != None):
            if(tempEnvGlobal.Global.get(id) != None):
                return tempEnvGlobal.Global.get(id).getValue()
            tempEnvGlobal = tempEnvGlobal.father
        print("Error: la variable " + id + " no existe")
        return None

    def alterVariable(self, id: str, value: Symbol,linea,columna):
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                tempVar: Symbol = tempEnv.variable.get(id)
                tempVar.value = value.getValue()
                self.variable[id] = tempVar
                return
            tempEnv = tempEnv.father
        print("Error: la variable " + id + " no existe",linea,columna)
        return None

    def alterVariableGlobal(self, id: str, value: Symbol,linea,columna):
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.Global.get(id) != None):
                tempVar: Symbol = tempEnv.Global.get(id)
                tempVar.value = value.getValue()
                self.Global[id] = tempVar
                return
            tempEnv = tempEnv.father
        print("Error: la variable " + id + " no existe",linea,columna)
        return None

    def saveFunction(self, id: str, function,linea,columna):
        if (self.function.get(id) != None):
            print("La función " + id + " ya existe",linea,columna)
            return
        self.function[id] = function
    
    def getFunction(self, id: str,linea,columna):
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.function.get(id) != None):
                return tempEnv.function.get(id)
            tempEnv = tempEnv.father
        print("Error: la función " + id + " no existe",linea,columna)
        return None