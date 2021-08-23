#Contiene toda la información que vamos a necesitar
class Symbol:
    #Nuestros simbolos poseen un id, un valor y un tipo
    def __init__(self, id: str, value, type):
        self.id = id
        self.value = value
        self.type = type

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getType(self):
        return self.type