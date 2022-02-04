class Symbol:
    #Nuestros simbolos poseen un id, un valor y un tipo
    #id - tipo - ambito - visibilidad - tama - posición - rol
    #x    int    father   global        1      0          varaible
    def __init__(self, id: str, type,ambito,visibilidad,tama, position,rol, valor):
        self.id = id
        self.Tipo = type
        self.Ambito=ambito
        self.Visibilidad=visibilidad
        self.Tama=tama
        self.Position = position
        self.Rol=rol
        self.value=valor

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getTipo(self):
        return self.type

    def getAmbito(self):
        return self.Ambito
    
    def getVisibilidad(self):
        return self.Visibilidad
    
    def getTama(self):
        return self.Tama
    
    def getPosition(self):
        return self.Visibilidad

    def getRol(self):
        return self.Rol

    def getValue(self):
        return self.value