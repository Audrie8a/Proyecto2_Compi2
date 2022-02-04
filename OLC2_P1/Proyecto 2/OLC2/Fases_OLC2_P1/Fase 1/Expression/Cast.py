from Enum.typeExpression import typeExpression
from Enum.castOperation import castOperation
from Environment.Environment import Environment
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Listas import Listas
class Cast(Expression):

    def __init__(self, leftExp: Expression, type, operation: castOperation,linea, columna):
        self.leftExp = leftExp
        self.type = type
        self.operation = operation
        self.linea=linea
        self.columna=columna

    
    def execute(self, environment: Environment) -> Symbol:
        # Resolvemos la expresion que viene de lado izquierdo
        leftValue = self.leftExp.execute(environment)
        line=self.linea
        column=self.columna
        Error=""
        
        try:
            if(self.operation == castOperation.PARSE):          
                if self.type==typeExpression.INTEGER: 
                    return Symbol(
                        "",
                        int(leftValue.getValue()),
                        typeExpression.INTEGER,"",line,column
                    )
                elif self.type==typeExpression.FLOAT: 
                    return Symbol(
                        "",
                        float(leftValue.getValue()),
                        typeExpression.FLOAT,"",line,column
                    )
                elif self.type==typeExpression.BOOL: 
                    return Symbol(
                        "",
                        bool(leftValue.getValue()),
                        typeExpression.BOOL,"",line,column
                    )
                elif self.type==typeExpression.CHAR: 
                    return Symbol(
                        "",
                        str(leftValue.getValue())[0],
                        typeExpression.CHAR,"",line,column
                    )
                elif self.type==typeExpression.STRING: 
                    return Symbol(
                        "",
                        str(leftValue.getValue()),
                        typeExpression.STRING,"",line,column
                    )
                else:
                    Error=("\nError al castear, no se reconoció el tipo de dato!")
                    print("\nError al castear, no se reconoció el tipo de dato!")
                    Listas.saveError("Error al castear, no se reconoció el tipo de dato!",line,column)
                    return Symbol(                    
                        "",
                        None,
                        typeExpression.STRING,"",line,column
                    )
            elif(self.operation == castOperation.TYPEOF):
                if leftValue.getType().value==0:
                    return Symbol(
                            "",
                            "String",
                            typeExpression.STRING,"",line,column
                        )
                elif leftValue.getType().value==1:
                    return Symbol(
                            "",
                            "Int64",
                            typeExpression.STRING,"",line,column
                        )
                elif leftValue.getType().value==2:
                    return Symbol(
                            "",
                            "Float64",
                            typeExpression.STRING,"",line,column
                        )
                elif leftValue.getType().value==3:
                    return Symbol(
                            "",
                            "Bool",
                            typeExpression.STRING,"",line,column
                        )
                elif  leftValue.getType().value==6:
                    return Symbol(
                            "",
                            "Char",
                            typeExpression.STRING,"",line,column
                        )
                else:                    
                    Error=("\nNo fue posible ubicar el tipo de dato al que pertenece esta expresion " + str(leftValue.getValue()))
                    print("\nNo fue posible ubicar el tipo de dato al que pertenece esta expresion " + str(leftValue.getValue()))
                    Listas.saveError("No fue posible ubicar el tipo de dato al que pertenece esta expresion " + str(leftValue.getValue()),line,column)
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING,"",line,column
                    )

            elif(self.operation == castOperation.TRUNC):
                if leftValue.getType().value==2 :
                    return Symbol(
                            "",
                            int(leftValue.getValue()),
                            typeExpression.INTEGER,"",line,column
                        )
                else:                    
                    Error=("\nNo es posible truncar otros tipos de datos que no sean Float : " + str(leftValue.getValue()))
                    print("\nNo es posible truncar otros tipos de datos que no sean Float : " + str(leftValue.getValue()))
                    Listas.saveError("No es posible truncar otros tipos de datos que no sean Float : " + str(leftValue.getValue()),line,column)
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING,"",line,column
                    )
            
            elif(self.operation == castOperation.STRING):
                return Symbol(
                            "",
                            str(leftValue.getValue()),
                            typeExpression.STRING,"",line,column
                        )
            elif(self.operation == castOperation.FLOAT):
                if leftValue.getType().value==1:
                    return Symbol(
                                "",
                                float(leftValue.getValue()),
                                typeExpression.FLOAT,"",line,column
                            )
                else:
                    print("\nNo es posible convertir a Float otros tipos de datos que no sean Enteros : " + str(leftValue.getValue()))
                    Error=("\nNo es posible convertir a Float otros tipos de datos que no sean Enteros : " + str(leftValue.getValue()))
                    Listas.saveError("No es posible convertir a Float otros tipos de datos que no sean Enteros : " + str(leftValue.getValue()),line,column)
                    return Symbol(
                            "",
                            None,
                            typeExpression.STRING,"",line,column
                    )

        except:
            Listas.saveError(Error,line,column)
            return Symbol('',None,typeExpression.STRING,"",line,column)
                