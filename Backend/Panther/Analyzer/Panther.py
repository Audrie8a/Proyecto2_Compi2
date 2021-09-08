# -----------------------------------------------------------------------------
# Rainman Sián
# 07-02-2020
#
# Ejemplo mi primer proyecto con Python utilizando ply en Ubuntu
# -----------------------------------------------------------------------------
linea =0
columna =0
reservadas={
    'while'     :   'RWHILE',
    'function'  :   'RFUNCTION',
    'end'       :   'REND',

    'print'     :   'IPRINT',
    'println'   :   'IPRINTLN',


    'Int64'     :   'RINT',
    'Float64'   :   'RFLOAT',
    'Bool'      :   'RBOOL',
    'Char'      :   'RCHAR',
    'String'    :   'RSTRING',


    'parse'     :   'IPARSE',
    'typeof'    :   'RTYPEOF',
    'trunc'     :   'RTRUNC',
    'float'     :   'RFLOATC',

    'uppercase' :   'IUPPERCASE',
    'lowercase' :   'ILOWERCASE',


    'log10'     :   'ILOGD',
    'log'       :   'ILOG',
    'sin'       :   'ISIN',
    'cos'       :   'ICOS',
    'tan'       :   'ITAN',
    'sqrt'      :   'ISQRT',
    'string'    :   'ISTRING',

    'true'      :   'VERDADERO',
    'false'     :   'FALSO',

    'global'    :   'RGLOBAL',
    'local'     :   'RLOCAL',
}

tokens  = [
    

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
    'CHAR',


    'PTCOMA',
    'COMA',  
    'FPTS',
    'IGUAL',
    'ID',

    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'NOIGUAL',


    'NOT',
    'AND',
    'OR'
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
t_FPTS           = r'::'
t_IGUAL          = r'='

t_MAYOR     = r'>'
t_MENOR     = r'<'
t_MAYORIGUAL     = r'>='
t_MENORIGUAL     = r'<='
t_IGUALIGUAL     = r'=='
t_NOIGUAL        = r'!='
t_NOT            = r'!'
t_AND            = r'&&'
t_OR             = r'\|\|'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

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

def t_CHAR(t):
    r'\'.?\''
    t.value = t.value[1:-1]
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
from types import DynamicClassAttribute
from Environment.Environment import Environment
from Instruction.IPrint import IPrint
from Instruction.IPrintln import IPrintln
from Instruction.Declaration import Declaration 
from Instruction.DeclaracionSinTipo import DeclaracionSinTipo
from Instruction.VariableCall import VariableCall
from Instruction.Function import Function
from Instruction.Parameter import Parameter
from Instruction.CallFuncSt import CallFuncSt
from Instruction.While import While
from Expression.Primitive import Primitive
from Expression.Arithmetic import Arithmetic
from Expression.Logic import Logic
from Expression.Concat import Concat
from Expression.Native import Native
from Expression.Cast import Cast
from Expression.Relational import Relational
from Enum.arithmeticOperation import arithmeticOperation
from Enum.relationalOperation import relationalOperation
from Enum.concatOperation import concatOperation
from Enum.nativeOperation import nativeOperation
from Enum.logicOperation import logicOperation
from Enum.castOperation import castOperation
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
    ''' instruccion     :   impresion PTCOMA
                            | expresionL
                            | ciclo PTCOMA
                            | asignacion PTCOMA
                            | DecFunc PTCOMA
                            | callFunc PTCOMA
                            | empty
    '''
    if t[1]==False:
        t[0]=IPrintln(Primitive(" ", typeExpression.STRING))
    else:
        t[0] = t[1]

#------------------------------------------------------------------
def p_DecFunc(t):
    '''DecFunc    : RFUNCTION ID PARIZQ Parametros PARDER block REND
                    | RFUNCTION ID PARIZQ PARDER block REND
    '''
    if len(t)==8:
        t[0]=Function(t[2],t[4],t[6])
    elif len(t)==7:
        t[0]=Function(t[2],None,t[5])
#------------------------------------------------------------------
def p_Parametros(t):
    '''Parametros   :   Parametros COMA Parametro
                        | Parametro
    '''
    if(len(t) == 4):
        t[1].append(t[3])
        t[0] = t[1]
    elif(len(t) == 2):
        t[0] = [t[1]]


#------------------------------------------------------------------
def p_Parametro(t):
    '''Parametro    :   ID FPTS Tipo
                        | ID
    '''
    if len(t)==4:
        t[0]=Parameter(t[1],t[3])
    elif len(t)==2:
        t[0]=Parameter(t[1],typeExpression.OBJETO)

#-----------------------------------------------------------------
def p_callFunc(t):
    ''' callFunc    :   ID  ParametrosFunc 
    '''
    t[0] = CallFuncSt(t[1],t[2])

#-----------------------------------------------------------------
def p_ParametrosFunc(t):
    ''' ParametrosFunc  : PARIZQ lstVal PARDER
                        | PARIZQ PARDER
    '''
    if len(t)==4: t[0]=t[2]
    elif len(t)==3: t[0]=[] # -> AQUÍ ESTÁ EL ERROR

#-----------------------------------------------------------------
def p_lstVal(t):
    ''' lstVal  :   lstVal COMA expresionL
                    | expresionL
    '''
    if(len(t) == 4):
        t[1].append(t[3])
        t[0] = t[1]
    elif(len(t) == 2):
        t[0] = [t[1]]

#-----------------------------------------------------------------
def p_ciclo(t):
    ''' ciclo     :   whileSt
    '''
    t[0] = t[1]

#-----------------------------------------------------------------
def p_whileSt(t):
    ''' whileSt     :   RWHILE expresionL block REND 
    '''
    t[0]= While(t[2],t[3])

#------------------------------------------------------------------
def p_block(t):
    '''block    : instrucciones
    '''
    t[0]=t[1]

#------------------------------------------------------------------

def p_asignacion(t):
    '''asignacion   :   TipoVarible ID asingArray IGUAL expresionL Final
                        | ID asingArray IGUAL expresionL Final
    '''
    if len(t)==7:
        if t[3]==False:     # Si no es un arreglo
            if t[6]==False:  # Si no define tipo variable
                t[0]=DeclaracionSinTipo(t[1],t[2],t[5],False,linea, columna)
            else:           # Si define tipo variable
                t[0]=Declaration(t[1],t[2],t[6],t[5],False,linea, columna)            
        else: pass          # Si es un arreglo
    else:
        if t[2]==False:     # Si no es un arreglo
            if t[5]==False:  # Si no define tipo variable
                t[0]=DeclaracionSinTipo("Vacio",t[1],t[4],False,linea, columna)
            else:           # Si define tipo variable
                t[0]=Declaration("Vacio",t[1],t[5],t[4],False,linea, columna)            
        else: pass          # Si es un arreglo


def p_TipoVarible(t):
    '''TipoVarible   :  RGLOBAL
                        | RLOCAL
    '''
    
    t[0]= t[1]

#------------------------------------------------------------------
def p_asingArray(t):
    '''asingArray   :   asingArray PARIZQ ENTERO PARDER
                    |   empty   
    '''
    if len(t)==5: 
        t[0]=True
    elif len(t)==2: 
        t[0]=t[1]
#------------------------------------------------------------------
def p_Final(t):
    '''Final    :   FPTS Tipo
                    | empty
    '''
    if len(t)==3:
        t[0]=t[2]
    else:
        t[0]=t[1]
#------------------------------------------------------------------
def p_Tipo(t):
    '''Tipo :   RINT
                | RFLOAT
                | RBOOL
                | RCHAR
                | RSTRING   
    '''
    
    if t[1]=='Int64'        : t[0]=typeExpression.INTEGER
    elif t[1]=='Float64'    : t[0]=typeExpression.FLOAT
    elif t[1]=='Bool'       : t[0]=typeExpression.BOOL
    elif t[1]=='Char'       : t[0]=typeExpression.CHAR
    elif t[1]=='String'     : t[0]=typeExpression.STRING 
    
#-----------------------------------------------------------------
def p_impresion(t):
    ''' impresion   :   IPRINT PARIZQ val PARDER 
                        | IPRINTLN PARIZQ val PARDER 
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
        if t[2] == '&&'  : t[0] = Logic( t[1], t[3], logicOperation.AND,linea,columna)
        elif t[2] == '||': t[0] = Logic(t[1], t[3], logicOperation.OR,linea,columna)
        elif t[1] ==  '!': t[0] = Logic(t[2], t[2], logicOperation.NOT,linea,columna)
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
        if t[2] == '>'  : t[0] = Relational( t[1], t[3], relationalOperation.MAYORQ,linea,columna)
        elif t[2] == '<': t[0] = Relational(t[1], t[3], relationalOperation.MENORQ,linea,columna)
        elif t[2] == '>=': t[0] = Relational(t[1], t[3], relationalOperation.MAYORIGUAL,linea,columna)
        elif t[2] == '<=': t[0] = Relational(t[1], t[3], relationalOperation.MENORIGUAL,linea,columna)      
        elif t[2] == '==': t[0] = Relational(t[1], t[3], relationalOperation.IGUALIGUAL,linea,columna)      
        elif t[2] == '!=': t[0] = Relational(t[1], t[3], relationalOperation.DIFERENTE,linea,columna)
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

def p_valor_char(t):
    '''valor    : CHAR
    '''
    t[0] = Primitive(t[1], typeExpression.CHAR)

def p_valor_string(t):
    '''valor   :    cadena                   
    '''
    t[0]= t[1]

def p_valor_nativas(t):
    '''valor    :   nativas
    '''
    t[0]=t[1]

def p_valor_Id (t):
    '''valor    : ID
    '''
    t[0]=VariableCall(t[1])

def p_empty(t):
     'empty :'
     t[0]=False
    
#-------------------------------------------------------------------
def p_nativas(t):
    '''nativas  :   ILOGD PARIZQ expresion PARDER
                    | ILOG PARIZQ expresion COMA expresion PARDER
                    | ISIN PARIZQ expresion PARDER
                    | ICOS PARIZQ expresion PARDER
                    | ITAN PARIZQ expresion PARDER
                    | ISQRT PARIZQ expresion PARDER
                    | casteo
    '''
    if len(t)==5:
        if t[1]=='log10': t[0]=Native(t[3],t[3],nativeOperation.LOGD, linea,columna)
        elif t[1]=='sin': t[0]=Native(t[3],t[3],nativeOperation.SIN, linea,columna)
        elif t[1]=='cos': t[0]=Native(t[3],t[3],nativeOperation.COS, linea,columna)
        elif t[1]=='tan': t[0]=Native(t[3],t[3],nativeOperation.TAN, linea,columna)
        elif t[1]=='sqrt': t[0]=Native(t[3],t[3],nativeOperation.SQRT, linea,columna)
    elif len(t)==7:
        t[0]=Native(t[3],t[5],nativeOperation.LOG, linea,columna)
    elif len(t)==2:
        t[0]=t[1]
        
#--------------------------------------------------------------------
def p_casteo(t):
    '''casteo   :   IPARSE PARIZQ Tipo COMA expresionL PARDER
                    | RTRUNC PARIZQ RINT COMA expresionL PARDER
                    | RTYPEOF PARIZQ expresionL PARDER                    
                    | ISTRING PARIZQ expresionL PARDER
                    | RFLOATC PARIZQ expresionL PARDER
    '''
    if len(t)==7:
        if t[1]=='parse': t[0]=Cast(t[5],t[3],castOperation.PARSE)
        elif t[1]=='trunc': t[0]=Cast(t[5],typeExpression.FLOAT,castOperation.TRUNC)
    elif len(t)==5:
        if t[1]=='typeof': t[0]=Cast(t[3],typeExpression.OBJETO,castOperation.TYPEOF)
        elif t[1]=='string': t[0]=Cast(t[3], typeExpression.OBJETO,castOperation.STRING)
        elif t[1]=='float': t[0]=Cast(t[3],typeExpression.OBJETO,castOperation.FLOAT)

#--------------------------------------------------------------------
def p_cadena(t):
    '''cadena   :   IUPPERCASE PARIZQ expresion PARDER
                    | ILOWERCASE PARIZQ expresion PARDER
                    | IPARSE PARIZQ ISTRING COMA expresionL PARDER
                    | STRING
    '''
    if len(t)==5:
        if t[1]=='uppercase': t[0]=Concat(t[3],t[3],concatOperation.UPPERCASE)
        elif t[1]=='lowercase': t[0]=Concat(t[3],t[3],concatOperation.LOWERCASE)
    elif len(t)==7:
        t[0]= Concat(t[5],t[5],concatOperation.PARSE)#Primitive(t[5],typeExpression.STRING)
    elif len(t)==2: 
        t[0]=Primitive(t[1],typeExpression.STRING)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

