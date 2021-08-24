# -----------------------------------------------------------------------------
# Rainman Sián
# 07-02-2020
#
# Ejemplo mi primer proyecto con Python utilizando ply en Ubuntu
# -----------------------------------------------------------------------------

tokens  = (
    'IPRINT',
    'IPRINTLN',
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'DECIMAL',
    'ENTERO',
    'STRING',
    'PTCOMA',
    'COMA',
    'IPARSE',
    'ISTRING'
)

# Tokens
t_IPRINT     = r'print'
t_IPRINTLN   = r'println' 
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_PTCOMA    = r';'
t_COMA      = r','
t_IPARSE    = r'parse'
t_ISTRING   = r'string'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value=t.value[1:-1]
    return t

# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Construyendo el analizador léxico
from Environment.Environment import Environment
from Instruction.IPrint import IPrint
from Instruction.IPrintln import IPrintln
from Expression.Primitive import Primitive
from Expression.Arithmetic import Arithmetic
from Enum.arithmeticOperation import arithmeticOperation
from Enum.typeExpression import typeExpression
from Expression.Concat import Concat
from Enum.concatOperation import concatOperation

import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('right','UMENOS'),
    )

# Definición de la gramática
def p_initial(t):
    '''initial  :   instrucciones'''
    glovalEnv= Environment (None)
    for ins in t[1]:
        ins.execute(glovalEnv)

#-----------------------------------------------------------------
def p_instrucciones_lista(t):
    '''instrucciones    :   instrucciones instruccion
                            | instruccion
     '''

    if(len(t)==3):
        t[1].append(t[2])
        t[0]=t[1]
    elif (len(t)==2):
        t[0]=[t[1]]

#-----------------------------------------------------------------
def p_instruccion(t):
    ''' instruccion     :   impresion
    '''
    t[0] = t[1]

#-----------------------------------------------------------------
def p_impresion(t):
    ''' impresion   :   IPRINT PARIZQ val PARDER PTCOMA
                        | IPRINTLN PARIZQ val PARDER PTCOMA
    '''
    if t[1] =='print'       : t[0]=IPrint(t[3])
    elif t[1]=='println'    : t[0]=IPrintln(t[3])

#-----------------------------------------------------------------
def p_val(t):
    ''' val     :   val COMA val
                    | casteo POR casteo
                    | expresion                   
    '''
    if len(t)==4 and t[2]==',': t[0]= Concat(t[1],t[3],concatOperation.COMA)
    elif len(t)==2: t[0]=t[1]
#-----------------------------------------------------------------
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion'''
    if t[2] == '+'  : t[0] = Arithmetic( t[1], t[3], arithmeticOperation.PLUS)
    elif t[2] == '-': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MINUS)
    elif t[2] == '*': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MULTIPLY)
    elif t[2] == '/': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.DIV)

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_entero(t):
    '''expresion    : ENTERO
    '''
    t[0] = Primitive(t[1], typeExpression.INTEGER)

def p_expresion_decimal(t):
    '''expresion    : DECIMAL
    '''
    t[0] = Primitive(t[1], typeExpression.FLOAT)

def p_expresion_string(t):
    '''expresion    : STRING
    '''
    t[0] = Primitive(t[1], typeExpression.STRING)

def p_expresion_string_casteo(t):
    '''casteo   :   IPARSE PARIZQ ISTRING COMA ENTERO PARDER
                    | IPARSE PARIZQ ISTRING COMA DECIMAL PARDER
    '''
    t[0]= Primitive( t[5], typeExpression.STRING)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
