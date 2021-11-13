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
    'if'        :   'RIF',
    'elseif'      :   'RELIF',
    'else'      :   'RELSE',
    'return'    :   'RRETURN',
    'continue'  :   'RCONTINUE',
    'break'     :   'RBREAK',
    'nothing'   :   'RNOTHING',

    'mutable'   :   'RMUTABLE',
    'struct'     :   'RSTRUCT',
    'length'    :   'RLENGTH',
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
    'ID',  
    
    'FPTS',
    'IGUAL',

    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'NOIGUAL',

    'PTO',


    'NOT',
    'AND',
    'OR',

    'CORDER',
    'CORIZQ'
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

t_PTO            = r'.'

t_CORDER         = r'\]'
t_CORIZQ         = r'\['


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
from Environment.Symbol import Symbol
from Environment.Listas import Listas
from types import DynamicClassAttribute
from Environment.Environment import Environment
from Instruction.IPrint import IPrint
from Instruction.IPrintln import IPrintln
from Instruction.Declaration import Declaration 
from Instruction.DeclaracionSinTipo import DeclaracionSinTipo,SoloDeclaracion
from Instruction.VariableCall import VariableCall
from Instruction.Function import Function
from Instruction.Parameter import Parameter
from Instruction.CallFuncSt import CallFuncSt
from Instruction.While import While
from Instruction.ifSt import ifSt
from Instruction.DecStruct import DecStruct
from Instruction.atributosStruct import atributosStruct
from Instruction.callStruct import callStruct
from Instruction.asignStructs import asignStructs
from Instruction.arreglo import arreglo
from Instruction.callArreglo import callArreglo
from Instruction.length import length
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
    glovalEnv= Environment (None,"global")
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
                            | condicion PTCOMA
                            | stransferencia PTCOMA
                            | DecStructs PTCOMA
                            | asignStructs PTCOMA
                            | arreglo PTCOMA
                            | empty
    '''
    if t[1]==False:
        t[0]=IPrintln(Primitive(" ", typeExpression.STRING,linea,columna),t.lineno(1),linea)
    else:
        t[0] = t[1]

#------------------------------------------------------------------
def p_DecFunc(t):
    '''DecFunc    : RFUNCTION ID PARIZQ Parametros PARDER block REND
                    | RFUNCTION ID PARIZQ PARDER block REND
    '''
    if len(t)==8:
        t[0]=Function(t[2],t[4],t[6],t.lineno(1),t.lexpos(1))
    elif len(t)==7:
        t[0]=Function(t[2],None,t[5],t.lineno(1),t.lexpos(1))
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
        t[0]=Parameter(t[1],t[3],t.lineno(1),t.lexpos(1))
    elif len(t)==2:
        t[0]=Parameter(t[1],typeExpression.OBJETO,t.lineno(1),t.lexpos(1))

#-----------------------------------------------------------------
def p_callFunc(t):
    ''' callFunc    :   ID  ParametrosFunc 
    '''
    t[0] = CallFuncSt(t[1],t[2],t.lineno(1),t.lexpos(1))

#-----------------------------------------------------------------
def p_ParametrosFunc(t):
    ''' ParametrosFunc  : PARIZQ lstVal PARDER
                        | PARIZQ PARDER
    '''
    if len(t)==4: t[0]=t[2]
    elif len(t)==3: t[0]=[] # -> AQUÍ ESTÁ EL ERROR
#--------------------------------------------------------------------
def p_arreglo(t):
    '''arreglo  :   TipoVarible ID IGUAL CORIZQ lstarreglos CORDER
                    | ID IGUAL CORIZQ lstarreglos CORDER
    '''
    if len(t)==7:
        t[0]=arreglo(t[2],t[5],t[1],t.lineno(1),t.lexpos(1))
    elif len(t)==6:
        t[0]=arreglo(t[1],t[4],None,t.lineno(1),t.lexpos(1))
    


#--------------------------------------------------------------------
def p_lstarreglos(t):
    '''lstarreglos  :   lstarreglos COMA CORIZQ lstVal CORDER
                        | CORIZQ lstarreglos CORDER 
                        | lstarreglos COMA expresionL
                        | expresionL
    '''
    if(len(t) == 6):
        t[1].append(t[4])
        t[0] = t[1]
    elif(len(t) == 4):
        if t[2]!=',':
            t[0] = [t[2]]
        else:
            t[1].append(t[3])
            t[0]=t[1]
    else:
        t[0]=[t[1]]

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
def p_DecStructs(t):
    ''' DecStructs  :   RMUTABLE RSTRUCT ID blockAtributos REND
                        | RSTRUCT ID blockAtributos REND 
    '''
    if len(t)==5: #Inmutable
        t[0]=DecStruct(None,t[2],t[3],t.lineno(1),t.lexpos(1))
    else: #Mutable
        t[0]=DecStruct(t[1],t[3],t[4],t.lineno(1),t.lexpos(1))

#-----------------------------------------------------------------
def p_asignStructs(t):
    ''' asignStructs    :   ID PTO ID IGUAL expresionL
    '''
    t[0]=asignStructs(t[1],t[3],t[5],t.lineno(1),t.lexpos(1))

#-----------------------------------------------------------------
def p_blockAtributos(t):
    ''' blockAtributos  :   blockAtributos  blockAtributo
                            | blockAtributo
    '''
    if(len(t)==3):
        t[1].append(t[2])
        t[0]=t[1]
    elif (len(t)==2):
        t[0]=[t[1]]
#-----------------------------------------------------------------
def p_blockAtributo(t):
    ''' blockAtributo   :   ID FPTS Tipo PTCOMA
                            | ID PTCOMA
    '''
    if len(t)==5:
        t[0]=atributosStruct(t[1],t[3],t.lineno(1),t.lexpos(1))
    else:
        t[0]=atributosStruct(t[1],typeExpression.OBJETO,t.lineno(1),t.lexpos(1))

        
#-----------------------------------------------------------------
def p_ciclo(t):
    ''' ciclo     :   whileSt
    '''
    t[0] = t[1]

#-----------------------------------------------------------------
def p_whileSt(t):
    ''' whileSt     :   RWHILE expresionL block REND 
    '''
    t[0]= While(t[2],t[3],t.lineno(1),t.lexpos(1))

#-----------------------------------------------------------------
def p_codndicion(t):
    ''' condicion   :   RIF expresionL block REND
                        | RIF expresionL block RELSE block REND
                        | RIF expresionL block elifList REND
    '''
    if len(t)==5:
        t[0]=ifSt(t[2],t[3],None,t.lineno(1),t.lexpos(0))
    elif len(t)==7:
        t[0]=ifSt(t[2],t[3],t[5],t.lineno(1),t.lexpos(0))
    elif len(t)==6:
        t[0]=ifSt(t[2],t[3],t[4],t.lineno(1),t.lexpos(0))

#-----------------------------------------------------------------
def p_elifList(t):
    ''' elifList    :   RELIF expresionL block
                        | RELIF expresionL block RELSE block
                        | RELIF expresionL block elifList
    '''
    if len(t)==4:
        t[0]=ifSt(t[2],t[3],None,t.lineno(1),t.lexpos(0))
    elif len(t)==6:
        t[0]=ifSt(t[2],t[3],t[5],t.lineno(1),t.lexpos(0))
    elif len(t)==5:
        t[0]=ifSt(t[2],t[3],t[4],t.lineno(1),t.lexpos(0))


#------------------------------------------------------------------
def p_block(t):
    '''block    : instrucciones
    '''
    t[0]=t[1]
#------------------------------------------------------------------
def p_strasnferencia(t):
    '''stransferencia   :   RRETURN expresionL
                            | RRETURN
                            | RBREAK
                            | RCONTINUE
    '''
    if len(t)==3 and t[1]=='return':
        t[0]=Symbol("return",t[2],typeExpression.OBJETO,"",t.lineno(1),t.lexpos(1))
    elif len(t)==2 and t[1]=='return':
        t[0]=Symbol("return",Primitive(0,typeExpression.INTEGER,t.lineno(1),t.lexpos(1)),typeExpression.OBJETO,"",t.lineno(1),t.lexpos(1))
    elif t[1]=='break':
        t[0]=Symbol("break",Primitive(0,typeExpression.INTEGER,t.lineno(1),t.lexpos(1)),typeExpression.OBJETO,"",t.lineno(1),t.lexpos(1))
    elif t[1]=='continue':
        t[0]=Symbol("continue","continue",typeExpression.OBJETO,"",t.lineno(1),t.lexpos(1))

#------------------------------------------------------------------

def p_asignacion(t):
    '''asignacion   :   TipoVarible ID  IGUAL expresionL Final
                        | TipoVarible ID
                        | ID IGUAL expresionL Final
    '''
    if len(t)==6:
        if t[5]==False:  # Si no define tipo variable
            t[0]=DeclaracionSinTipo(t[1],t[2],t[4],False,t.lineno(1), t.lexpos(2))
        else:           # Si define tipo variable
            t[0]=Declaration(t[1],t[2],t[5],t[4],False,t.lineno(1), t.lexpos(2))
    elif len(t)==3:         
        t[0]=SoloDeclaracion(t[1],t[2],False,t.lineno(1),t.lexpos(2))
    else:
        if t[4]==False:  # Si no define tipo variable
            t[0]=DeclaracionSinTipo("Vacio",t[1],t[3],False,t.lineno(1), t.lexpos(2))
        else:           # Si define tipo variable
            t[0]=Declaration("Vacio",t[1],t[4],t[3],False,t.lineno(1), t.lexpos(2))

    
#--------------------------------------------------------------------
def p_TipoVarible(t):
    '''TipoVarible   :  RGLOBAL
                        | RLOCAL
    '''
    
    t[0]= t[1]


#------------------------------------------------------------------
def p_lstAsingArrays(t):
    ''' lstAsingArrays  :   lstAsingArrays lstAsingArray
                            | lstAsingArray
    '''
    if(len(t)==3):
        t[1].append(t[2])
        t[0]=t[1]
    elif (len(t)==2):
        t[0]=[t[1]]
#------------------------------------------------------------------
def p_lstAsignArray(t):
    '''lstAsingArray    :   CORIZQ expresionL CORDER
    '''
    t[0]=t[2]
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
    if t[1] =='print'       : t[0]=IPrint(t[3],t.lineno(1),t.lexpos(0))
    elif t[1]=='println'    : t[0]=IPrintln(t[3],t.lineno(1),t.lexpos(0))

#-----------------------------------------------------------------
def p_val(t):
    ''' val     :   val COMA val   
                    | expresionL   
                    
                       
    '''
    if len(t)==2: t[0]=t[1]
    elif len(t)==4 and t[2]==',': t[0]=Concat(t[1],t[3], concatOperation.COMMA,t.lineno(1),t.lexpos(2))

#-----------------------------------------------------------------
def p_expresion_logica(t):
    '''expresionL : expresionL AND expresionL
                  | expresionL OR expresionL
                  | NOT expresionL
                  | PARIZQ expresionL PARDER
                  | expresionR
    '''
    if len(t)==4:
        if t[2] == '&&'  : t[0] = Logic( t[1], t[3], logicOperation.AND,t.lineno(1),t.lexpos(2))
        elif t[2] == '||': t[0] = Logic(t[1], t[3], logicOperation.OR,t.lineno(1),t.lexpos(2))
        elif t[1] == '(': t[0]=t[2]
    
    elif len(t)==3:
         t[0] = Logic(t[2], t[2], logicOperation.NOT,t.lineno(2),t.lexpos(0))
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
        if t[2] == '>'  : t[0] = Relational( t[1], t[3], relationalOperation.MAYORQ,t.lineno(2),t.lexpos(0))
        elif t[2] == '<': t[0] = Relational(t[1], t[3], relationalOperation.MENORQ,t.lineno(2),t.lexpos(0))
        elif t[2] == '>=': t[0] = Relational(t[1], t[3], relationalOperation.MAYORIGUAL,t.lineno(2),t.lexpos(0))
        elif t[2] == '<=': t[0] = Relational(t[1], t[3], relationalOperation.MENORIGUAL,t.lineno(2),t.lexpos(0))      
        elif t[2] == '==': t[0] = Relational(t[1], t[3], relationalOperation.IGUALIGUAL,t.lineno(2),t.lexpos(0))      
        elif t[2] == '!=': t[0] = Relational(t[1], t[3], relationalOperation.DIFERENTE,t.lineno(2),t.lexpos(0))
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
        if t[2] == '+'  : t[0] = Arithmetic( t[1], t[3], arithmeticOperation.PLUS,t.lineno(1),t.lexpos(2))
        elif t[2] == '-': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MINUS,t.lineno(1),t.lexpos(2))
        elif t[2] == '/': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.DIV,t.lineno(1),t.lexpos(2))
        elif t[2] == '*': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MULTIPLY,t.lineno(1),t.lexpos(2))
        elif t[2] == '^': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.POW,t.lineno(1),t.lexpos(2))
        elif t[2] == '%': t[0] = Arithmetic(t[1], t[3], arithmeticOperation.MOD,t.lineno(1),t.lexpos(2))  
        elif t[1] == '(': t[0]=t[2]
    elif t[1]=='-':
        t[0]=Arithmetic(t[2],t[2],arithmeticOperation.UMENOS,t.lineno(1),t.lexpos(2))      
    elif len(t)==2:        
        t[0]=t[1]
    
#------------------------------------------------------------------

def p_booleano(t):
    ''' booleano    :   VERDADERO
                        | FALSO
    '''
    t[0]= Primitive(t[1],typeExpression.BOOL,t.lineno(1),t.lexpos(0))

def p_valor_entero(t):
    '''valor    : ENTERO
    '''
    t[0] = Primitive(t[1], typeExpression.INTEGER,t.lineno(1),t.lexpos(0))

def p_valor_decimal(t):
    '''valor    : DECIMAL
    '''
    t[0] = Primitive(t[1], typeExpression.FLOAT,t.lineno(1),t.lexpos(0))

def p_valor_char(t):
    '''valor    : CHAR
    '''
    t[0] = Primitive(t[1], typeExpression.CHAR,t.lineno(1),t.lexpos(0))

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
    t[0]=VariableCall(t[1],t.lineno(1),t.lexpos(0))

def p_valor_Struct (t):
    '''valor    : ID PTO ID
    '''
    t[0]=callStruct(t[1],t[3],t.lineno(1),t.lexpos(0))


def p_valor_funcion(t):
    ''' valor   : callFunc
    '''
    t[0]=t[1]

def p_valor_arreglo(t):
    ''' valor   : ID lstAsingArrays  
    '''
    t[0]=callArreglo(t[1],t[2],t.lineno(1),t.lexpos(1))

def p_valor_Vacio(t):
    ''' valor   : RNOTHING
    '''
    t[0]=Primitive(None, typeExpression.STRING,t.lineno(1),t.lexpos(0))

def p_valor_length(t):
    ''' valor   :   RLENGTH PARIZQ ID PARDER
                |   RLENGTH PARIZQ ID lstAsingArrays PARDER
    '''
    if len(t)==5:
        t[0]=length(t[3],t.lineno(1),t.lexpos(1))
    else:
        t[3]=callArreglo(t[3],t[4],t.lineno(1),t.lexpos(1))
        t[0]=length(t[3],t.lineno(1),t.lexpos(1))

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
        if t[1]=='log10': t[0]=Native(t[3],t[3],nativeOperation.LOGD, t.lineno(1),t.lexpos(2))
        elif t[1]=='sin': t[0]=Native(t[3],t[3],nativeOperation.SIN, t.lineno(1),t.lexpos(2))
        elif t[1]=='cos': t[0]=Native(t[3],t[3],nativeOperation.COS, t.lineno(1),t.lexpos(2))
        elif t[1]=='tan': t[0]=Native(t[3],t[3],nativeOperation.TAN, t.lineno(1),t.lexpos(2))
        elif t[1]=='sqrt': t[0]=Native(t[3],t[3],nativeOperation.SQRT, t.lineno(1),t.lexpos(2))
    elif len(t)==7:
        t[0]=Native(t[3],t[5],nativeOperation.LOG, t.lineno(1),t.lexpos(2))
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
        if t[1]=='parse': t[0]=Cast(t[5],t[3],castOperation.PARSE,t.lineno(1),t.lexpos(2))
        elif t[1]=='trunc': t[0]=Cast(t[5],typeExpression.FLOAT,castOperation.TRUNC,t.lineno(1),t.lexpos(2))
    elif len(t)==5:
        if t[1]=='typeof': t[0]=Cast(t[3],typeExpression.OBJETO,castOperation.TYPEOF,t.lineno(1),t.lexpos(2))
        elif t[1]=='string': t[0]=Cast(t[3], typeExpression.OBJETO,castOperation.STRING,t.lineno(1),t.lexpos(2))
        elif t[1]=='float': t[0]=Cast(t[3],typeExpression.OBJETO,castOperation.FLOAT,t.lineno(1),t.lexpos(2))

#--------------------------------------------------------------------
def p_cadena(t):
    '''cadena   :   IUPPERCASE PARIZQ expresionL PARDER
                    | ILOWERCASE PARIZQ expresionL PARDER
                    | IPARSE PARIZQ ISTRING COMA expresionL PARDER
                    | STRING
    '''
    if len(t)==5:
        if t[1]=='uppercase': t[0]=Concat(t[3],t[3],concatOperation.UPPERCASE,t.lineno(1),t.lexpos(2))
        elif t[1]=='lowercase': t[0]=Concat(t[3],t[3],concatOperation.LOWERCASE,t.lineno(1),t.lexpos(2))
    elif len(t)==7:
        t[0]= Concat(t[5],t[5],concatOperation.PARSE,t.lineno(1),t.lexpos(2))#Primitive(t[5],typeExpression.STRING)
    elif len(t)==2: 
        t[0]=Primitive(t[1],typeExpression.STRING,linea,columna)

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    Listas.saveError("Error sintáctico en '%s'" % t.value,0,0)
    
    


import ply.yacc as yacc
parser = yacc.yacc()

