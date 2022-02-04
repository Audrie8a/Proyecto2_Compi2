  
from Environment.Symbol import Symbol
from Expression.Primitive import Primitive
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas

class callStruct(Expression):

    def __init__(self, id: str,atributo:str,linea,columna) -> None:
        self.id = id
        self.atributo=atributo
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment) -> Symbol:
        try:
            retValue = environment.getValorStruct(self.id,self.atributo,self.linea,self.columna)

            if(retValue == None):
                retValue = Primitive(0,typeExpression.INTEGER,self.linea,self.columna).execute(environment)

            return retValue
        except:
            print("\nError al llamar valor struct!")
            Listas.saveError("Error al llamar valor struct!",self.linea,self.columna)