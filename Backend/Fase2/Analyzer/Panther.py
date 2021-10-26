reservadas = {
    'print'     :   'IPRINT',
    'println'   :   'IPRINTLN',


    # 'Int64'     :   'RINT',
    # 'Float64'   :   'RFLOAT',
    # 'Bool'      :   'RBOOL',
    # 'Char'      :   'RCHAR',
    # 'String'    :   'RSTRING'
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
#    'COMA',
    'ID'
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
#t_COMA      = r','



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

# def t_CHAR(t):
#     r'\'.?\''
#     t.value = t.value[1:-1]
#     return t

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
from Expression.Arithmetic.Plus import Plus
from Expression.Arithmetic.Minus import Minus
from Expression.Arithmetic.Multiply import Multiply
from Expression.Arithmetic.Division import Division
from Expression.Primitive.VariableCall import VariableCall
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Generator.Generator import Generator
from Instructions.Declaration import Declaration

import Analyzer.ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
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
                            | expresion
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
    ''' impresion   :   IPRINT PARIZQ expresion PARDER 
                        | IPRINTLN PARIZQ expresion PARDER 
    '''
    if t[1] =='print'       : t[0]=IPrint(t[3])
    elif t[1]=='println'    : t[0]=IPrintln(t[3])


#====================================================

#====================================================

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
        # elif t[2] == '*': t[0] = 
        # elif t[2] == '^': t[0] = 
        # elif t[2] == '%': t[0] = 
        # elif t[1] == '(': t[0]=t[2]
    #elif t[1]=='-':
        #t[0]=Arithmetic(t[2],t[2],arithmeticOperation.UMENOS,t.lineno(1),t.lexpos(2))      
    elif len(t)==2:        
        t[0]=t[1]
#====================================================
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
    t[0]= None

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