from src.interprete.compilador.simbolos.SimboloArray import SimboloArray
from src.interprete.compilador.expresiones.natives.Truncate import Truncate
from src.interprete.compilador.expresiones.AccesoArray import AccesoArray
from src.interprete.compilador.expresiones.AccesoFuncion import AccesoFuncion
from src.interprete.compilador.expresiones.AccesoStruct import AccesoStruct
from src.interprete.compilador.expresiones.AccesoVa import AccesoVariable
from src.interprete.compilador.expresiones.Aritmetica import Aritmetica
from src.interprete.compilador.expresiones.Array import Arreglo
from src.interprete.compilador.expresiones.Length import Length
from src.interprete.compilador.expresiones.Logica import Logica
from src.interprete.compilador.expresiones.natives.UpLow import ToUpLowCase
from src.interprete.compilador.expresiones.Primitivo import Primitivo
from src.interprete.compilador.expresiones.Relacional import Relacional
from src.interprete.compilador.instrucciones.array.AsignAccessArray import (
    AsignarAccesoArray,
)
from src.interprete.compilador.instrucciones.control.For import For
from src.interprete.compilador.instrucciones.control.IF import If
from src.interprete.compilador.instrucciones.control.While import While
from src.interprete.compilador.instrucciones.function.Function import Funcion
from src.interprete.compilador.instrucciones.Print import Print
from src.interprete.compilador.instrucciones.Statement import Statement
from src.interprete.compilador.instrucciones.struct.AsignarAccesoStruct import (
    AsignarAccesoStruct,
)
from src.interprete.compilador.instrucciones.struct.Struct import Struct
from src.interprete.compilador.instrucciones.tranferencia.Break import Break
from src.interprete.compilador.instrucciones.tranferencia.Continue import (
    Continue,
)
from src.interprete.compilador.instrucciones.tranferencia.Return import Return
from src.interprete.compilador.instrucciones.variable.Asignacion import (
    Asignacion,
)
from src.interprete.compilador.simbolos.Parametro import Parametro
from src.interprete.compilador.tipos.Tipo import (
    TipoArtimetico,
    TipoLogico,
    TipoRelational,
    TipoScoope,
    TipoStruct,
    TipoUpLowCase,
    TipoVar,
)

# ==============================================================================
# PALABRAS RESERVADAS
# ==============================================================================
reservadas = {
    # INSTRUCCIONES
    'print': 'RPRINT',
    'println': 'RPRINTLN',
    'if': 'RIF',
    'elseif': 'RELSEIF',
    'else': 'RELSE',
    'while': 'RWHILE',
    'break': 'RBREAK',
    'continue': 'RCONTINUE',
    'for': 'RFOR',
    'function': 'RFUNCTION',
    'return': 'RRETURN',
    # RESERVADAS
    'global': 'RGLOBAL',
    'local': 'RLOCAL',
    'true': 'RTRUE',
    'false': 'RFALSE',
    'uppercase': 'RUPPER',
    'lowercase': 'RLOWER',
    'Int64': 'RINT64',
    'Float64': 'RFLOAT64',
    'Bool': 'RBOOL',
    'Char': 'RCHAR',
    'String': 'RSTRING',
    'void': 'RVOID',
    'in': 'RIN',
    'end': 'REND',
    'struct': 'RSTRUCT',
    'mutable': 'RMUTABLE',
    'length': 'RLENGTH',
    'Vector': 'RVECTOR',
    'trunc': 'RTRUNCN',
}
# ==============================================================================
# TOKENS
# ==============================================================================
tokens = [
    # SIMBOLOS
    'PUNTO',
    'PCOMA',
    'PARA',
    'PARC',
    'COMA',
    'IGUAL',
    'DPUNTOS',
    'CORA',
    'CORC',
    'LLA',
    'LLC',
    # ARITMETICOS
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MODULO',
    # RELACIONAL
    'MAYORQ',
    'MENORQ',
    'MAYORI',
    'MENORI',
    'COMPARACION',
    'DIFERENTE',
    # LOGICO
    'OR',
    'AND',
    'NOT',
    # TIPO
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
] + list(reservadas.values())
# -------------- -> TOKEN SIMBOLOS <- --------------
t_PUNTO = r'\.'
t_PARA = r'\('
t_PARC = r'\)'
t_COMA = r','
t_PCOMA = r';'
t_DPUNTOS = r'\:'
t_IGUAL = r'='
t_CORA = r'\['
t_CORC = r'\]'
t_LLA = r'\{'
t_LLC = r'\}'
# -------------- -> TOKEN ARITMETICOS <- --------------
t_MAS = r'\+'
t_MENOS = r'\-'
t_POR = r'\*'
t_DIV = r'\/'
t_MODULO = r'\%'
t_POT = r'\^'
# -------------- -> TOKEN RELACIONAL <- --------------
t_MAYORQ = r'>'
t_MENORQ = r'<'
t_MAYORI = r'>='
t_MENORI = r'<='
t_COMPARACION = r'=='
t_DIFERENTE = r'!='
# -------------- -> TOKEN LOGICO <- --------------
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
# -------------- -> TOKEN DECIMAL <- --------------
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Float value too large %d', t.value)
        t.value = 0
    return t


# -------------- -> TOKEN ENTERO <- --------------
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Integer value too large %d', t.value)
        t.value = 0
    return t


# -------------- -> TOKEN ID <- --------------
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')  # Check for reserved words
    return t


# -------------- -> TOKEN CADENA <- --------------
def t_CADENA(t):
    r'\"(\\"|.)*?\"'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace("\\'", '\'')
    return t


# ==============================================================================
# COMENTARIOS
# ==============================================================================
# Múltiples líneas #= ... =#
def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')


# Simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'(\#.*\n)|(\#.*)'
    t.lexer.lineno += 1
    pass


# ==============================================================================
# OTROS
# ==============================================================================
# Caracteres ignorados
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    if t.value[0] != ' ':
        print(t.value[0])
        print(
            "Illegal character '%s'" % t.value[0],
            t.lexer.lineno,
            (find_column(input_data, t)),
        )
    t.lexer.skip(1)


def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


import src.interprete.ply.lex as lex

lexer = lex.lex()

# -------------- -> PRECENDENCIA <- --------------
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    (
        'left',
        'COMPARACION',
        'DIFERENTE',
        'MAYORQ',
        'MENORQ',
        'MAYORI',
        'MENORI',
    ),
    ('left', 'MAS', 'MENOS'),
    ('left', 'DIV', 'POR', 'MODULO'),
    ('nonassoc', 'POT'),
    ('right', 'UNOT'),
    ('right', 'UMENOS'),
)

# ==============================================================================


# ANALISIS SINTACTICO


# ==============================================================================


def p_init(t):
    'init               : instrucciones'
    t[0] = t[1]


def p_instrucciones_lista(t):
    'instrucciones      : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    'instrucciones      : instruccion'
    t[0] = [t[1]]


def p_statement(t):
    '''statement        : instrucciones'''
    t[0] = Statement(t[1], t.lineno(1), t.lexpos(0))


# ==============================================================================
# INSTRUCCION
# ==============================================================================
def p_inst(t):
    '''
    instruccion         : print_inst fin_inst
                        | asign_inst fin_inst
                        | if_inst fin_inst
                        | while_inst fin_inst
                        | for_inst fin_inst
                        | function_inst fin_inst
                        | call_funct_inst fin_inst
                        | struct_inst fin_inst
                        | assign_atr_struct fin_inst
                        | break_inst fin_inst
                        | continue_inst fin_inst
                        | return_inst fin_inst
                        | asig_access_array fin_inst
    '''
    t[0] = t[1]


def p_fin_inst(t):
    '''
    fin_inst            : PCOMA
                        |
    '''
    if len(t) == 2 or len(t) == 1:
        t[0] = ';'


# ------------------------------------------------------------------------------
# PRINTLN
def p_inst_print(t):
    '''
    print_inst          : RPRINT PARA expresion_list PARC
                        | RPRINT PARA PARC
    '''
    if len(t) == 5:
        t[0] = Print(t[3], t.lineno(1), find_column(input_data, t.slice[1]))
    else:
        t[0] = Print([], t.lineno(1), find_column(input_data, t.slice[1]))


def p_inst_println(t):
    '''
    print_inst          : RPRINTLN PARA expresion_list PARC
                        | RPRINTLN PARA PARC
    '''
    if len(t) == 5:
        t[0] = Print(
            t[3], t.lineno(1), find_column(input_data, t.slice[1]), True
        )
    else:
        t[0] = Print([], t.lineno(1), find_column(input_data, t.slice[1]), True)


# ------------------------------------------------------------------------------
# ASIGNACION
def p_inst_asignacion(t):
    '''
    asign_inst          : ID IGUAL expresion DPUNTOS DPUNTOS tipo
                        | ID IGUAL expresion
                        | RGLOBAL ID IGUAL expresion
                        | RLOCAL ID IGUAL expresion
                        | RGLOBAL ID IGUAL expresion DPUNTOS DPUNTOS tipo
                        | RLOCAL ID IGUAL expresion DPUNTOS DPUNTOS tipo
    '''
    # ID IGUAL expresion DPUNTOS DPUNTOS tipo
    if len(t) == 7:
        t[0] = Asignacion(
            t[1], t[6], t[3], t.lineno(2), find_column(input_data, t.slice[2])
        )
    # ID IGUAL expresion
    elif len(t) == 4:
        t[0] = Asignacion(
            t[1], None, t[3], t.lineno(2), find_column(input_data, t.slice[2])
        )
    elif len(t) == 5:
        # RGLOBAL ID IGUAL expresion
        if t[1] == 'global':
            t[0] = Asignacion(
                t[2],
                None,
                t[4],
                t.lineno(3),
                find_column(input_data, t.slice[3]),
                TipoScoope.GLOBAL,
            )
        # RLOCAL ID IGUAL expresion
        elif t[1] == 'local':
            t[0] = Asignacion(
                t[2],
                None,
                t[4],
                t.lineno(3),
                find_column(input_data, t.slice[3]),
                TipoScoope.LOCAL,
            )
    elif len(t) == 8:
        # RGLOBAL ID IGUAL expresion DPUNTOS DPUNTOS tipo
        if t[1] == 'global':
            t[0] = Asignacion(
                t[2],
                t[7],
                t[4],
                t.lineno(3),
                find_column(input_data, t.slice[3]),
                TipoScoope.GLOBAL,
            )
        # RLOCAL ID IGUAL expresion DPUNTOS DPUNTOS tipo
        else:
            t[0] = Asignacion(
                t[2],
                t[7],
                t[4],
                t.lineno(3),
                find_column(input_data, t.slice[3]),
                TipoScoope.LOCAL,
            )


# ------------------------------------------------------------------------------
# IF
def p_inst_if(t):
    '''
    if_inst             : RIF expresion statement REND
                        | RIF expresion statement RELSE statement REND
                        | RIF expresion statement else_if_list REND
    '''
    if len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]))
    elif len(t) == 7:
        t[0] = If(
            t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]), t[5]
        )
    elif len(t) == 6:
        t[0] = If(
            t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]), t[4]
        )


def p_inst_if_elseif(t):
    '''
    else_if_list        : RELSEIF expresion statement
                        | RELSEIF expresion statement RELSE statement
                        | RELSEIF expresion statement else_if_list
    '''
    if len(t) == 4:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]))
    elif len(t) == 6:
        t[0] = If(
            t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]), t[5]
        )
    elif len(t) == 5:
        t[0] = If(
            t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1]), t[4]
        )


# ------------------------------------------------------------------------------
# WHILE
def p_inst_while(t):
    '''
    while_inst          : RWHILE expresion statement REND
    '''
    if len(t) == 5:
        if t[1] == 'while':
            t[0] = While(
                t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1])
            )


# ------------------------------------------------------------------------------
# TRANSEFERENCIA

# BREAK
def p_inst_break(t):
    'break_inst         : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input_data, t.slice[1]))


# CONTINUE
def p_inst_continue(t):
    'continue_inst      : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input_data, t.slice[1]))


# Return
def p_inst_return(t):
    '''
    return_inst         : RRETURN
                        | RRETURN expresion
    '''
    if len(t) == 2:
        t[0] = Return(None, t.lineno(1), find_column(input_data, t.slice[1]))
    else:
        t[0] = Return(t[2], t.lineno(1), find_column(input_data, t.slice[1]))


# ------------------------------------------------------------------------------
# FOR

# for normal
def p_inst_for(t):
    '''
    for_inst            : RFOR ID RIN expresion DPUNTOS expresion statement REND
                        | RFOR ID RIN expresion statement REND
    '''
    if len(t) == 9:
        t[0] = For(
            t[2],
            t[4],
            t[7],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
            t[6],
        )
    else:
        t[0] = For(
            t[2], t[4], t[5], t.lineno(1), find_column(input_data, t.slice[1])
        )


# ------------------------------------------------------------------------------
# FUNCIONES


def p_tipo_ret(t):
    '''
    tipo_return         : DPUNTOS DPUNTOS tipo_funct
                        |
    '''
    if len(t) == 4:
        t[0] = t[3]
    else:
        t[0] = TipoVar.VOID


def p_inst_func(t):
    '''
    function_inst       : RFUNCTION ID PARA PARC tipo_return statement REND
                        | RFUNCTION ID PARA list_param PARC tipo_return statement REND
    '''
    if len(t) == 8:
        t[0] = Funcion(
            t[2],
            [],
            t[6],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
            t[5],
        )
    else:
        t[0] = Funcion(
            t[2],
            t[4],
            t[7],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
            t[6],
        )


def p_list_param(t):
    '''
    list_param          : list_param COMA parametro
                        | parametro
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]


def p_param(t):
    '''
    parametro           : ID DPUNTOS DPUNTOS tipo
    '''
    t[0] = Parametro(t[1], t[4])


def p_inst_call_funct(t):
    '''
    call_funct_inst     : ID PARA PARC
                        | ID PARA expresion_list PARC
    '''
    if len(t) == 4:
        t[0] = AccesoFuncion(
            t[1], [], t.lineno(1), find_column(input_data, t.slice[1])
        )
    else:
        t[0] = AccesoFuncion(
            t[1], t[3], t.lineno(1), find_column(input_data, t.slice[1])
        )


def p_exp_call_funct(t):
    '''
    call_funct_exp      : ID PARA PARC
                        | ID PARA expresion_list PARC
    '''
    if len(t) == 4:
        t[0] = AccesoFuncion(
            t[1], [], t.lineno(1), find_column(input_data, t.slice[1])
        )
    else:
        t[0] = AccesoFuncion(
            t[1], t[3], t.lineno(1), find_column(input_data, t.slice[1])
        )


# ------------------------------------------------------------------------------
# STRUCT
def p_inst_struct(t):
    '''
    struct_inst         : RSTRUCT ID att_list REND
                        | RMUTABLE RSTRUCT ID att_list REND
    '''
    if len(t) == 5:
        t[0] = Struct(
            t[2], t[3], t.lineno(1), find_column(input_data, t.slice[1])
        )
    else:
        t[0] = Struct(
            t[3],
            t[4],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
            TipoStruct.MUTABLE,
        )


# Lista de atributos
def p_att_list(t):
    '''
    att_list            : att_list att_item
                        | att_item
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]


def p_att_item(t):
    '''
    att_item            : ID DPUNTOS DPUNTOS tipo PCOMA
    '''
    t[0] = Parametro(t[1], t[4])


# Acceso Struct
def p_exp_access_struct(t):
    'access_struct      : ID PUNTO list_att_id'
    t[0] = AccesoStruct(
        t[1], t[3], t.lineno(1), find_column(input_data, t.slice[1])
    )


def p_list_att_id(t):
    '''
    list_att_id         : list_att_id PUNTO ID
                        | ID
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]


# Asignar Acceso a Struct
def p_inst_assing_acces_struc(t):
    'assign_atr_struct  : ID PUNTO list_att_id IGUAL expresion'
    t[0] = AsignarAccesoStruct(
        t[1], t[3], t[5], t.lineno(2), find_column(input_data, t.slice[2])
    )


# ------------------------------------------------------------------------------
# ARREGLO
def p_inst_assing_acces_array(t):
    '''
    asig_access_array   : ID list_position IGUAL expresion
    '''
    t[0] = AsignarAccesoArray(
        t[1], t[2], t[4], t.lineno(3), find_column(input_data, t.slice[3])
    )


# ==============================================================================
# EXPRESIONES
# ==============================================================================
def p_exp_unaria(t):
    '''
    expresion           : MENOS expresion %prec UMENOS
                        | NOT expresion %prec UNOT
    '''
    if t[1] == '-':
        t[0] = Aritmetica(
            TipoArtimetico.UMENOS,
            None,
            t[2],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
        )
    elif t[1] == '!':
        t[0] = Logica(
            TipoLogico.NOT,
            None,
            t[2],
            t.lineno(1),
            find_column(input_data, t.slice[1]),
        )


def p_exp_agrupacion(t):
    'expresion          : PARA expresion PARC'
    t[0] = t[2]


def p_exp_list(t):
    '''
    expresion_list      : expresion_list COMA expresion
                        | expresion
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]


def p_exp_binaria(t):
    '''
    expresion           : expresion MAS expresion
                        | expresion MENOS expresion
                        | expresion POR expresion
                        | expresion DIV expresion
                        | expresion POT expresion
                        | expresion MODULO expresion
                        | expresion MAYORQ expresion
                        | expresion MENORQ expresion
                        | expresion MAYORI expresion
                        | expresion MENORI expresion
                        | expresion COMPARACION expresion
                        | expresion DIFERENTE expresion
                        | expresion OR expresion
                        | expresion AND expresion
    '''
    # -------------- -> (+) <- --------------
    if t[2] == '+':
        t[0] = Aritmetica(
            TipoArtimetico.SUMA,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (-) <- --------------
    elif t[2] == '-':
        t[0] = Aritmetica(
            TipoArtimetico.RESTA,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (*) <- --------------
    elif t[2] == '*':
        t[0] = Aritmetica(
            TipoArtimetico.POR,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (/) <- --------------
    elif t[2] == '/':
        t[0] = Aritmetica(
            TipoArtimetico.DIV,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (^) <- --------------
    elif t[2] == '^':
        t[0] = Aritmetica(
            TipoArtimetico.POT,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (%) <- --------------
    elif t[2] == '%':
        t[0] = Aritmetica(
            TipoArtimetico.MODULO,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (>) <- --------------
    elif t[2] == '>':
        t[0] = Relacional(
            TipoRelational.MAYORQ,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (<) <- --------------
    elif t[2] == '<':
        t[0] = Relacional(
            TipoRelational.MENORQ,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (>=) <- --------------
    elif t[2] == '>=':
        t[0] = Relacional(
            TipoRelational.MAYORI,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (<=) <- --------------
    elif t[2] == '<=':
        t[0] = Relacional(
            TipoRelational.MENORI,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (==) <- --------------
    elif t[2] == '==':
        t[0] = Relacional(
            TipoRelational.COMPARACION,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (!=) <- --------------
    elif t[2] == '!=':
        t[0] = Relacional(
            TipoRelational.DIFERENTE,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (||) <- --------------
    elif t[2] == '||':
        t[0] = Logica(
            TipoLogico.OR,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )

    # -------------- -> (&&) <- --------------
    elif t[2] == '&&':
        t[0] = Logica(
            TipoLogico.AND,
            t[1],
            t[3],
            t.lineno(2),
            find_column(input_data, t.slice[2]),
        )


def p_exp_fin(t):
    '''
    expresion           : ENTERO
                        | DECIMAL
                        | RTRUE
                        | RFALSE
                        | CADENA
                        | ID
                        | call_funct_exp
                        | array_exp
                        | acces_array
                        | access_struct
                        | len_array
                        | truncate_exp
    '''
    if len(t) == 2:
        if t.slice[1].type == 'ENTERO':
            t[0] = Primitivo(
                int(t[1]),
                TipoVar.INT64,
                t.lineno(1),
                find_column(input_data, t.slice[1]),
            )
        elif t.slice[1].type == 'DECIMAL':
            t[0] = Primitivo(
                float(t[1]),
                TipoVar.FLOAT64,
                t.lineno(1),
                find_column(input_data, t.slice[1]),
            )
        elif t.slice[1].type == 'ID':
            t[0] = AccesoVariable(
                t[1], t.lineno(1), find_column(input_data, t.slice[1])
            )
        elif t.slice[1].type == 'call_funct_exp':
            t[0] = t[1]
        elif t.slice[1].type == 'array_exp':
            t[0] = t[1]
        elif t.slice[1].type == 'acces_array':
            t[0] = t[1]
        elif t.slice[1].type == 'access_struct':
            t[0] = t[1]
        elif t.slice[1].type == 'len_array':
            t[0] = t[1]
        elif t.slice[1].type == 'truncate_exp':
            t[0] = t[1]
        elif isinstance(t[1], str):
            value = t[1]
            if value == 'true':
                t[0] = Primitivo(
                    True,
                    TipoVar.BOOLEAN,
                    t.lineno(1),
                    find_column(input_data, t.slice[1]),
                )
            elif value == 'false':
                t[0] = Primitivo(
                    False,
                    TipoVar.BOOLEAN,
                    t.lineno(1),
                    find_column(input_data, t.slice[1]),
                )
            else:
                t[0] = Primitivo(
                    str(value),
                    TipoVar.STRING,
                    t.lineno(1),
                    find_column(input_data, t.slice[1]),
                )


def p_exp_uplow_case(t):
    '''
    expresion           : RUPPER PARA expresion PARC
                        | RLOWER PARA expresion PARC
    '''
    if len(t) == 5:
        if t[1] == 'uppercase':
            t[0] = ToUpLowCase(
                TipoUpLowCase.UPPER,
                t[3],
                t.lineno(1),
                find_column(input_data, t.slice[1]),
            )
        elif t[1] == 'lowercase':
            t[0] = ToUpLowCase(
                TipoUpLowCase.LOWER,
                t[3],
                t.lineno(1),
                find_column(input_data, t.slice[1]),
            )


# ------------------------------------------------------------------------------
# TIPO
# ------------------------------------------------------------------------------
# Tipo var
def p_tipo(t):
    '''
    tipo                : RINT64
                        | RFLOAT64
                        | RBOOL
                        | RCHAR
                        | RSTRING
                        | ID
                        | tipo_array_
    '''
    if len(t) == 2:
        if t[1] == 'Int64':
            t[0] = TipoVar.INT64

        elif t[1] == 'Float64':
            t[0] = TipoVar.FLOAT64

        elif t[1] == 'Bool':
            t[0] = TipoVar.BOOLEAN

        elif t[1] == 'Char':
            t[0] = TipoVar.CHAR

        elif t[1] == 'String':
            t[0] = TipoVar.STRING
        elif t.slice[1].type == 'ID':
            t[0] = t[1]
        elif t.slice[1].type == 'tipo_array_':
            t[0] = t[1]


# Tipo function
def p_tipo_funct(t):
    '''
    tipo_funct          : RINT64
                        | RFLOAT64
                        | RBOOL
                        | RCHAR
                        | RSTRING
                        | RVOID
                        | ID
    '''
    if len(t) == 2:
        if t[1] == 'Int64':
            t[0] = TipoVar.INT64

        elif t[1] == 'Float64':
            t[0] = TipoVar.FLOAT64

        elif t[1] == 'Bool':
            t[0] = TipoVar.BOOLEAN

        elif t[1] == 'Char':
            t[0] = TipoVar.CHAR

        elif t[1] == 'String':
            t[0] = TipoVar.STRING

        elif t[1] == 'void':
            t[0] = TipoVar.VOID

        elif t.slice[1].type == 'ID':
            t[0] = t[1]


# Vector{Vector{Int64}};
# Vector{Vector{Vector{Int64}}};
def p_tipo_array(t):
    '''
    tipo_array_         : RVECTOR LLA tipo_array_ LLC
                        | RVECTOR LLA subtipo_array LLC
    '''
    if t.slice[3].type == 'subtipo_array':
        t[0] = SimboloArray(TipoVar.ARRAY, t[3])
    else:
        t[0] = t[3]


def p_tipo_subtipo_arra(t):
    '''
    subtipo_array       : RINT64
                        | RFLOAT64
                        | RBOOL
                        | RCHAR
                        | RSTRING
    '''
    if len(t) == 2:
        if t[1] == 'Int64':
            t[0] = TipoVar.INT64

        elif t[1] == 'Float64':
            t[0] = TipoVar.FLOAT64

        elif t[1] == 'Bool':
            t[0] = TipoVar.BOOLEAN

        elif t[1] == 'Char':
            t[0] = TipoVar.CHAR

        elif t[1] == 'String':
            t[0] = TipoVar.STRING


# ------------------------------------------------------------------------------
# ARREGLO
def p_exp_array(t):
    '''
    array_exp           : CORA expresion_list CORC
    '''
    t[0] = Arreglo(t[2], t.lineno(1), find_column(input_data, t.slice[1]))


# ACCESO ARRELGLO
def p_exp_access_array(t):
    'acces_array        : ID list_position'
    t[0] = AccesoArray(
        t[1], t[2], t.lineno(1), find_column(input_data, t.slice[1])
    )


def p_list_position(t):
    '''
    list_position       : list_position position
                        | position
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]


def p_position(t):
    '''
    position            : CORA expresion CORC
    '''
    t[0] = t[2]


# lenght
def p_exp_length(t):
    'len_array          : RLENGTH PARA expresion PARC'
    t[0] = Length(t[3], t.lineno(1), find_column(input_data, t.slice[1]))


# ------------------------------------------------------------------------------
# TRUNCATE
def p_truncate(t):
    '''
    truncate_exp        : RTRUNCN PARA expresion PARC
    '''
    t[0] = Truncate(t[3], t.lineno(1), find_column(input_data, t.slice[1]))


# ==============================================================================
# PARSE
# ==============================================================================
import src.interprete.ply.yacc as yacc

parser = yacc.yacc()
input_data: str = ''


def parse(input_string: str):
    global lexer
    global parser
    lexer = lex.lex()
    parser = yacc.yacc()
    global input_data
    input_data = input_string
    return parser.parse(input_string)