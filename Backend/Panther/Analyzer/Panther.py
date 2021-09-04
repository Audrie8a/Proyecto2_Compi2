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
    'POW',
    'MOD',
    'PTCOMA',
    'COMA',
    'IPARSE',
    'ISTRING',
    'IUPPERCASE',
    'ILOWERCASE',
    'ILOGD',
    'ILOG',
    'ISIN',
    'ICOS',
    'ITAN',
    'ISQRT',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'NOIGUAL',
    'VERDADERO',
    'FALSO',
    'NOT',
    'AND',
    'OR'
)

# Tokens
t_IPRINT     = r'print'
t_IPRINTLN   = r'println' 
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
t_IPARSE    = r'parse'
t_ISTRING   = r'string'
t_IUPPERCASE    = r'uppercase'
t_ILOWERCASE     = r'lowercase'
t_ILOGD     = r'log10'
t_ILOG     = r'log'
t_ISIN      = r'sin'
t_ICOS      = r'cos'
t_ITAN      = r'tan'
t_ISQRT     = r'sqrt'
t_MAYOR     = r'>'
t_MENOR     = r'<'
t_MAYORIGUAL     = r'>='
t_MENORIGUAL     = r'<='
t_VERDADERO      = r'true'
t_FALSO     = r'false'
t_IGUALIGUAL     = r'=='
t_NOIGUAL        = r'!='
t_NOT            = r'!'
t_AND            = r'&&'
t_OR             = r'\|\|'

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

def t_MLCOMMENT(t):
    r'\#=(.|\n)*?=\#'
    

def t_OLCOMMENT(t):
    r'\#.*\n'
   

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
from Expression.Logic import Logic
from Expression.Concat import Concat
from Expression.Native import Native
from Expression.Relational import Relational
from Enum.arithmeticOperation import arithmeticOperation
from Enum.relationalOperation import relationalOperation
from Enum.concatOperation import concatOperation
from Enum.nativeOperation import nativeOperation
from Enum.logicOperation import logicOperation
from Enum.typeExpression import typeExpression

import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (  
    ('left','OR'),  
    ('left','AND'),
    ('left', 'MENOR','MENORIGUAL','MAYOR','MAYORIGUAL'),
    ('left','IGUALIGUAL','NOIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','POW','MOD'),
    ('right','UMENOS'),
    ('right','NOT'),
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
                            | expresion
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
                    | expresionL   
                    
                       
    '''
    if len(t)==2: t[0]=t[1]
    elif len(t)==4 and t[2]==',': t[0]=Concat(t[1],t[3], concatOperation.COMMA)

#-----------------------------------------------------------------
def p_expresion_logica(t):
    '''expresionL : expresionL AND expresionL
                  | expresionL OR expresionL
                  | NOT expresionL
                  | PARIZQ expresionL PARDER
                  | expresionR
    '''
    if len(t)==4:
        if t[2] == '&&'  : t[0] = Logic( t[1], t[3], logicOperation.AND)
        elif t[2] == '||': t[0] = Logic(t[1], t[3], logicOperation.OR)
        elif t[1] ==  '!': t[0] = Logic(t[2], t[2], logicOperation.NOT)
        elif t[1] == '(': t[0]=t[2]
    elif len(t)==2:
        t[0]=t[1]
    
#-----------------------------------------------------------------
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
        if t[2] == '>'  : t[0] = Relational( t[1], t[3], relationalOperation.MAYORQ)
        elif t[2] == '<': t[0] = Relational(t[1], t[3], relationalOperation.MENORQ)
        elif t[2] == '>=': t[0] = Relational(t[1], t[3], relationalOperation.MAYORIGUAL)
        elif t[2] == '<=': t[0] = Relational(t[1], t[3], relationalOperation.MENORIGUAL)      
        elif t[2] == '==': t[0] = Relational(t[1], t[3], relationalOperation.IGUALIGUAL)      
        elif t[2] == '!=': t[0] = Relational(t[1], t[3], relationalOperation.DIFERENTE)
        elif t[1] == '(': t[0]=t[2]
    elif len(t)==2:
        t[0]=t[1]
    
#------------------------------------------------------------------
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion DIVIDIDO expresion
                  | expresion POR expresion
                  | expresion POW expresion
                  | expresion MOD expresion                  
                  | MENOS expresion %prec UMENOS
                  | PARIZQ expresion PARDER
                  | valor
    '''
    if len(t)==4:
        if t[2] == '+'  : t[0] = Arithmetic( t[1], t[3], arithmeticOperation.PLUS)
        elif t[2] == '-': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MINUS)
        elif t[2] == '/': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.DIV)
        elif t[2] == '*': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MULTIPLY)
        elif t[2] == '^': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.POW)
        elif t[2] == '%': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MOD)  
        elif t[1] == '(': t[0]=t[2]
    elif t[1]=='-':
        t[0]=Arithmetic(t[2],t[2],arithmeticOperation.UMENOS)      
    elif len(t)==2:
        t[0]=t[1]
    
#------------------------------------------------------------------

def p_booleano(t):
    ''' booleano    :   VERDADERO
                        | FALSO
    '''
    t[0]= Primitive(t[1],typeExpression.BOOL)

def p_valor_entero(t):
    '''valor    : ENTERO
    '''
    t[0] = Primitive(t[1], typeExpression.INTEGER)

def p_valor_decimal(t):
    '''valor    : DECIMAL
    '''
    t[0] = Primitive(t[1], typeExpression.FLOAT)

def p_valor_string(t):
    '''valor   :    cadena                   
    '''
    t[0]= t[1]

def p_valor_nativas(t):
    '''valor    :   nativas
    '''
    t[0]=t[1]
#-------------------------------------------------------------------
def p_nativas(t):
    '''nativas  :   ILOGD PARIZQ expresion PARDER
                    | ILOG PARIZQ expresion COMA expresion PARDER
                    | ISIN PARIZQ expresion PARDER
                    | ICOS PARIZQ expresion PARDER
                    | ITAN PARIZQ expresion PARDER
                    | ISQRT PARIZQ expresion PARDER
    '''
    if len(t)==5:
        if t[1]=='log10': t[0]=Native(t[3],t[3],nativeOperation.LOGD)
        elif t[1]=='sin': t[0]=Native(t[3],t[3],nativeOperation.SIN)
        elif t[1]=='cos': t[0]=Native(t[3],t[3],nativeOperation.COS)
        elif t[1]=='tan': t[0]=Native(t[3],t[3],nativeOperation.TAN)
        elif t[1]=='sqrt': t[0]=Native(t[3],t[3],nativeOperation.SQRT)
    elif len(t)==7:
        t[0]=Native(t[3],t[5],nativeOperation.LOG)

#--------------------------------------------------------------------
def p_cadena(t):
    '''cadena   :   IUPPERCASE PARIZQ expresion PARDER
                    | ILOWERCASE PARIZQ expresion PARDER
                    | IPARSE PARIZQ ISTRING COMA ENTERO PARDER
                    | IPARSE PARIZQ ISTRING COMA DECIMAL PARDER
                    | STRING
    '''
    if len(t)==5:
        if t[1]=='uppercase': t[0]=Concat(t[3],t[3],concatOperation.UPPERCASE)
        elif t[1]=='lowercase': t[0]=Concat(t[3],t[3],concatOperation.LOWERCASE)
    elif len(t)==7:
        t[0]=Primitive(t[5],typeExpression.STRING)
    elif len(t)==2: 
        t[0]=Primitive(t[1],typeExpression.STRING)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

