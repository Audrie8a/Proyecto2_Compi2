  
from Environment.Symbol import Symbol
from Expression.Primitive import Primitive
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas

class asignStructs(Expression):

    def __init__(self, id: str,atributo:str,expresionL: typeExpression,linea,columna) -> None:
        self.id = id
        self.atributo=atributo
        self.value=expresionL
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment) -> Symbol:
        try:
            temporal =self.value.execute(environment)

            environment.alterValorStruct(self.id,self.atributo,temporal.getValue(),temporal.getType(),self.linea,self.columna)
        except:
            print("\nError al modificar valor struct!")
            Listas.saveError("Error al modificar valor struct!",self.linea,self.columna)