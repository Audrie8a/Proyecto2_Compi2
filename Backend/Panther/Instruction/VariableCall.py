  
from Environment.Symbol import Symbol
from Expression.Primitive import Primitive
from Environment.Environment import Environment
from Abstract.Expression import Expression
from Enum.typeExpression import typeExpression
from Environment.Listas import Listas

class VariableCall(Expression):

    def __init__(self, id: str,linea,columna) -> None:
        self.id = id
        self.linea=linea
        self.columna=columna

    def execute(self, environment: Environment) -> Symbol:
        try:
            retValue = environment.getVariable(self.id,self.linea,self.columna)

            if(retValue == None):
                retValue = Primitive(0,typeExpression.INTEGER,self.linea,self.columna).execute(environment)

            return retValue
        except:
            print("\nError al llamar variable!")
            Listas.saveError("Error al llamar variable!",self.linea,self.columna)