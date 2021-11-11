reservadas = {
    'print'     :   'IPRINT',
    'println'   :   'IPRINTLN',
    

    # 'Int64'     :   'RINT',
    # 'Float64'   :   'RFLOAT',
    # 'Bool'      :   'RBOOL',
    # 'Char'      :   'RCHAR',
    # 'String'    :   'RSTRING'

    'true'      :   'VERDADERO',
    'false'     :   'FALSO',
}

tokens = [
    'PARIZQ',
    'PARDER',

    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',

    'DECIMAL',
    'ENTERO',
    'STRING',
    'POW',
    'MOD',
#    'CHAR',


    'PTCOMA',
    'COMA',
    'ID',

    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'NOIGUAL'
 ] + list(reservadas.values())

# Tokens
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POW       = r'\^'
t_MOD       = r'%'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'

t_PTCOMA    = r';'
t_COMA      = r','


t_MAYOR     = r'>'
t_MENOR     = r'<'
t_MAYORIGUAL     = r'>='
t_MENORIGUAL     = r'<='
t_IGUALIGUAL     = r'=='
t_NOIGUAL        = r'!='


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
    t.value = t.value[1:-1]
    return t

def t_ID(t):
      r'[a-zA-Z_][a-zA-Z_0-9]*'
      t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
      return t

def t_CHAR(t):
     r'\'.?\''
     t.value = t.value[1:-1]
     return t

def t_MLCOMMENT(t):
    r'\#=(.|\n)*?=\#'
    

def t_OLCOMMENT(t):
    r'\#.*\n'

#Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
from Instructions.IPrint import IPrint
from Instructions.IPrintln import IPrintln
from Expression.Primitive.NumberVal import NumberVal
from Expression.Primitive.StringVal import StringVal
from Expression.Primitive.BooleanVal import BooleanVal
from Expression.Arithmetic.Plus import Plus
from Expression.Arithmetic.Minus import Minus
from Expression.Arithmetic.Multiply import Multiply
from Expression.Arithmetic.Division import Division
from Expression.Arithmetic.Pow import Pow
from Expression.Arithmetic.Mod import Mod
from Expression.Cadenas.Concat import Concat
from Expression.Relational.Menor import Menor
from Expression.Relational.Equal import Equal
from Expression.Relational.Mayor import Mayor
from Expression.Relational.MayorQue import MayorQue
from Expression.Relational.MenorQue import MenorQue
from Expression.Relational.NoIgual import NoIgual
from Expression.Primitive.VariableCall import VariableCall
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Generator.Generator import Generator
from Instructions.Declaration import Declaration

import Analyzer.ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left', 'MENOR','MENORIGUAL','MAYOR','MAYORIGUAL'),
    ('left','IGUALIGUAL','NOIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','POW','MOD'),
    ('right','UMENOS'),
    )

# Definición de la gramática=====================================================
def p_initial(t):
    '''initial : instructions'''

    generator: Generator = Generator()
    globalEnv = Environment(None)
    for ins in t[1]:
        ins.generator = generator
        ins.compile(globalEnv)

    
    t[0] = generator.getCode()

    #print(globalEnv.function)

#====================================================
def p_instructions(t):
    '''instructions : instructions instruction
                    | instruction
    '''
    if(len(t) == 3):
        t[1].append(t[2])
        t[0] = t[1]
    elif(len(t) == 2):
        t[0] = [t[1]]

#====================================================
def p_instruction(t):
    '''instruction     :    impresion PTCOMA
                            | expresionR
                            | empty
    '''
    t[0] = t[1]




#====================================================

# def p_Tipo(t):
#     '''Tipo :   RINT
#                 | RFLOAT
#                 | RBOOL
#                 | RCHAR
#                 | RSTRING   
#     '''
    
#     if t[1]=='Int64'        : t[0]=typeExpression.INTEGER
#     elif t[1]=='Float64'    : t[0]=typeExpression.FLOAT
#     elif t[1]=='Bool'       : t[0]=typeExpression.BOOL
#     elif t[1]=='Char'       : t[0]=typeExpression.CHAR
#     elif t[1]=='String'     : t[0]=typeExpression.STRING 
    

#====================================================
def p_impresion(t):
    ''' impresion   :   IPRINT PARIZQ val PARDER 
                        | IPRINTLN PARIZQ val PARDER 
    '''
    if t[1] =='print'       : t[0]=IPrint(t[3])
    elif t[1]=='println'    : t[0]=IPrintln(t[3])


#====================================================
def p_val(t):
    ''' val     :   val COMA val   
                    | expresionR                
    '''
    
    if(len(t)!=2):
        t[1].append(t[3])
        t[0]=t[1]
    else:
        t[0]=[t[1]]
#====================================================
def p_expresion_relacional(t):
    '''expresionR : expresionR MAYOR expresionR
                  | expresionR MENOR expresionR
                  | expresionR MAYORIGUAL expresionR
                  | expresionR MENORIGUAL expresionR
                  | expresionR IGUALIGUAL expresionR
                  | expresionR NOIGUAL expresionR
                  | PARIZQ expresionR PARDER
                  | booleano
                  | expresion
                  
    '''
    if len(t)==4:
        if t[2] == '<'  :   t[0]=Menor(t[1],t[3])
        elif t[2] == '>':   t[0]=Mayor(t[1],t[3])
        elif t[2] == '>=':  t[0]=MayorQue(t[1],t[3])
        elif t[2] == '<=':  t[0]=MenorQue(t[1],t[3])    
        elif t[2] == '==':  t[0]=Equal(t[1],t[3])     
        elif t[2] == '!=':  t[0]=NoIgual(t[1],t[3])
        elif t[1] == '(':   t[0]=t[2]
    elif len(t)==2:
        t[0]=t[1]
    
#====================================================
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion DIVIDIDO expresion
                  | expresion POR expresion
                  | expresion POW expresion
                  | expresion MOD expresion                  
                  | MENOS expresion %prec UMENOS 
                  | valor
    '''
    if len(t)==4:
        if t[2] == '+'  : t[0] = Plus(t[1],t[3])
        elif t[2] == '-': t[0] = Minus(t[1],t[3])
        elif t[2] == '/': t[0] = Division(t[1],t[3])
        elif t[2] == '*': t[0] = Multiply(t[1],t[3])
        elif t[2] == '^': t[0] = Pow(t[1],t[3])
        elif t[2] == '%': t[0] = Mod(t[1],t[3])
    elif t[1]=='-':
        t[0]=Minus( NumberVal(typeExpression.INTEGER,0),t[2])     
    elif len(t)==2:        
        t[0]=t[1]
#====================================================
def p_booleano(t):
    ''' booleano    :   VERDADERO
                        | FALSO
    '''
    t[0]=BooleanVal(typeExpression.BOOL,t[1])


def p_valor_agrupacion(t):
    'valor : PARIZQ expresion PARDER'
    t[0] = t[2]


def p_valor_entero(t):
    '''valor    : ENTERO
    '''
    t[0] = NumberVal(typeExpression.INTEGER,t[1])

def p_valor_decimal(t):
    '''valor    : DECIMAL
    '''
    t[0] = NumberVal(typeExpression.FLOAT,t[1])

def p_valor_string(t):
    '''valor   :    STRING                   
    '''
    t[0]= StringVal(typeExpression.STRING,t[1])

def p_valor_Id (t):
    '''valor    : ID
    '''
    t[0] = VariableCall(t[1])

def p_empty(t):
     'empty :'
     t[0]=False

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import Analyzer.ply.yacc as yacc
parser = yacc.yacc()