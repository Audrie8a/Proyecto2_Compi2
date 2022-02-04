from enum import Enum


class TipoVar(Enum):
    INT64 = 0           # Int (Integer)
    FLOAT64 = 1         # Float (Decimal)
    BOOLEAN = 2         # Boolean (True || False)
    CHAR = 3            # Char ('d')
    STRING = 4          # String ("Cadena")
    ERROR = 5
    NOTHING = 6         # Null (None)
    ARRAY = 7           # Array ([])
    STRUCT = 8          # Struct
    ANY = 9             # Cualquier Valor
    VOID = 10           # Tipo vacio


class TipoArtimetico(Enum):
    SUMA = 1            # Suma (+)
    RESTA = 2           # Resta (-)
    POR = 3             # Multiplicacion (*)
    DIV = 4             # Division (/)
    POT = 5             # Potencia (^)
    UMENOS = 6          # NEGATIVO (-)
    MODULO = 7          # Modulo (%)

class TipoRelational(Enum):
    MAYORQ = 1           # Mayor (>)
    MENORQ = 2           # Menor (<)
    MAYORI = 3           # Mayor Igual (>=)
    MENORI = 4           # Menor Igual (<=)
    COMPARACION = 5      # Comparacion (==)
    DIFERENTE = 6        # Diferente (!=)

class TipoLogico(Enum):
    OR = 1               # Or (||)
    AND = 2              # And (&&)
    NOT = 3              # Not (!)


class TipoPrint(Enum):
    CARACTER = 1        # "%c"
    FLOAT = 2           # "%g"
    INT = 3             # "%d"

class TipoUpLowCase(Enum):
    UPPER = 1           # Upper Case
    LOWER = 2           # Lower Case

class TipoScoope(Enum):
    GLOBAL = 1          # global
    LOCAL = 2           # local
    UNDEFINED = 3       # NO definido

class TipoStruct(Enum):
    MUTABLE = 1         # Permite cambios
    INMUTABLE = 2       # No permite cambios

    
def get_type_print(type_print: TipoPrint):
    if type_print == TipoPrint.CARACTER:
        return 'c', 'int'
    elif type_print == TipoPrint.INT:
        return 'd', 'int'
    return 'g', None



def get_tipo_var(type: TipoVar):
    if type == TipoVar.INT64:
        return 'Int64'
    elif type == TipoVar.FLOAT64:
        return 'Float64'
    elif type == TipoVar.BOOLEAN:
        return 'Bool'
    elif type == TipoVar.STRING:
        return 'String'
    elif type == TipoVar.CHAR:
        return 'Char'
    elif type == TipoVar.ARRAY:
        return 'Array'
    elif type == TipoVar.STRUCT:
        return 'Struct'
    elif type == TipoVar.ANY:
        return 'Any'
    elif type == TipoVar.VOID:
        return 'Void'
    else:
        return str(type)


def verify_type(left: TipoVar, right: TipoVar):
    # INT * x = ?
    if left == TipoVar.INT64:
        if right == TipoVar.INT64:
            return TipoVar.INT64
        elif right == TipoVar.FLOAT64:
            return TipoVar.FLOAT64
        else:
            return TipoVar.ERROR
    # Float * x = ?
    elif left == TipoVar.FLOAT64:
        if right == TipoVar.INT64:
            return TipoVar.FLOAT64
        elif right == TipoVar.FLOAT64:
            return TipoVar.FLOAT64
        else:
            return TipoVar.ERROR

    return TipoVar.ERROR