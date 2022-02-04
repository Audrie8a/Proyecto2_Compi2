#Contiene toda la información que vamos a necesitar
class Symbol:
    #Nuestros simbolos poseen un id, un valor y un tipo
    def __init__(self, id: str, value, type, extens, fila, columna):
        self.id = id
        self.value = value
        self.type = type
        self.extens = extens
        self.fila= fila
        self.columna= columna

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def getExtens(self):
        return self.extens

    def getLine(self):
        return self.fila
    
    def getColumn(self):
        return self.columna