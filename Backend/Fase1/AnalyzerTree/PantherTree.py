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
    'FPTS',
    'IGUAL',
    'ID',

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
from Node.Node import Node
from Instruction.Parameter import Parameter
from Instruction.CallFuncSt import CallFuncSt
from Instruction.Function import Function

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
    nodeInitial = Node("initial")
    nodeInitial.insertChild(t[1])

    f=open("./salida.txt")
    nodeInitial.getGraphAST()

#-----------------------------------------------------------------
def p_instrucciones_lista(t):
    '''instrucciones    :   instrucciones instruccion
                            | instruccion
     '''
    
    nodeInstrucciones = Node("instrucciones")
    if(len(t)==3):
        nodeInstrucciones.insertChild(t[1])
        nodeInstrucciones.insertChild(t[2])
    elif (len(t)==2):
        nodeInstrucciones.insertChild(t[1])
    t[0]=nodeInstrucciones

    
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
    nodeInstruction=Node("instruccion")
    if len(t)==2:
        nodeInstruction.insertChild(Node("empty"))
    else:
        nodeInstruction.insertChild(t[1])
        nodeInstruction.insertChild(Node(";"))
    t[0] = nodeInstruction

#------------------------------------------------------------------
def p_DecFunc(t):
    '''DecFunc    : RFUNCTION ID PARIZQ Parametros PARDER block REND
                    | RFUNCTION ID PARIZQ PARDER block REND
    '''
    
    nodeDecFunc= Node("DecFunc")
    if len(t)==8:
        nodeDecFunc.insertChild(Node("function"))
        nodeDecFunc.insertChild(Node(t[2]))
        nodeDecFunc.insertChild(Node("("))
        nodeDecFunc.insertChild(t[4])
        nodeDecFunc.insertChild(Node(")"))
        nodeDecFunc.insertChild(t[6])
        nodeDecFunc.insertChild(Node("end"))
    elif len(t)==7:
        nodeDecFunc.insertChild(Node("function"))
        nodeDecFunc.insertChild(Node(t[2]))
        nodeDecFunc.insertChild(Node("("))
        nodeDecFunc.insertChild(Node(")"))
        nodeDecFunc.insertChild(t[5])
        nodeDecFunc.insertChild(Node("end"))

    t[0]=nodeDecFunc
        
#------------------------------------------------------------------
def p_Parametros(t):
    '''Parametros   :   Parametros COMA Parametro
                        | Parametro
    '''
    nodeParametros = Node("Parametros")
    if(len(t) == 4):
        nodeParametros.insertChild(t[1])
        nodeParametros.insertChild(Node(","))
        nodeParametros.insertChild(t[3])
    elif(len(t) == 2):
        nodeParametros.insertChild(t[1])

    t[0]=nodeParametros

#------------------------------------------------------------------
def p_Parametro(t):
    '''Parametro    :   ID FPTS Tipo
                        | ID
    '''
    nodeParametro = Node("Parametro")
    if len(t)==4:
        nodeParametro.insertChild(Node(t[1]))
        nodeParametro.insertChild(t[2])
        nodeParametro.insertChild(t[3])
    elif len(t)==2:
        nodeParametro.insertChild(Node(t[1]))
    
    t[0]=nodeParametro

#-----------------------------------------------------------------
def p_callFunc(t):
    ''' callFunc    :   ID  ParametrosFunc 
    '''
    nodecallFunc=Node("callFunc")
    nodecallFunc.insertChild(Node(t[1]))
    nodecallFunc.insertChild(t[2])
    t[0]=nodecallFunc

#-----------------------------------------------------------------
def p_ParametrosFunc(t):
    ''' ParametrosFunc  : PARIZQ lstVal PARDER
                        | PARIZQ PARDER
    '''
    nodeParametrosFunc=Node("ParametrosFunc")
    if len(t)==4:
        nodeParametrosFunc.insertChild(Node("("))
        nodeParametrosFunc.insertChild(t[2])
        nodeParametrosFunc.insertChild(Node(")"))
    elif len(t)==3: 
        nodeParametrosFunc.insertChild(Node("("))
        nodeParametrosFunc.insertChild(Node(")"))

    t[0]=nodeParametrosFunc

#--------------------------------------------------------------------
def p_arreglo(t):
    '''arreglo  :   TipoVarible ID IGUAL CORIZQ lstarreglos CORDER
                    | ID IGUAL CORIZQ lstarreglos CORDER
    '''
    nodearreglo=Node("arreglo")
    if len(t)==7:
        nodearreglo.insertChild(t[1])
        nodearreglo.insertChild(Node(t[2]))
        nodearreglo.insertChild(Node("="))
        nodearreglo.insertChild(Node("["))
        nodearreglo.insertChild(Node("lstarreglos"))
        nodearreglo.insertChild(Node("]"))
    elif len(t)==6:
        nodearreglo.insertChild(Node(t[1]))
        nodearreglo.insertChild(Node("="))
        nodearreglo.insertChild(Node("["))
        nodearreglo.insertChild(Node("lstarreglos"))
        nodearreglo.insertChild(Node("]"))

    t[0]=nodearreglo
    


#--------------------------------------------------------------------
def p_lstarreglos(t):
    '''lstarreglos  :   lstarreglos COMA CORIZQ lstVal CORDER
                        | CORIZQ lstarreglos CORDER 
                        | lstarreglos COMA expresionL
                        | expresionL
    '''
    nodelstarreglos=Node("lstarreglos")
    if(len(t) == 6):
        nodelstarreglos.insertChild(t[1])
        nodelstarreglos.insertChild(Node(","))
        nodelstarreglos.insertChild(Node("["))
        nodelstarreglos.insertChild(t[4])
        nodelstarreglos.insertChild(Node("]"))
    elif(len(t) == 4):
        if t[2]!=',':
            nodelstarreglos.insertChild(Node("["))
            nodelstarreglos.insertChild(t[2])
            nodelstarreglos.insertChild(Node("]"))
        else:
            nodelstarreglos.insertChild(t[1])
            nodelstarreglos.insertChild(Node(","))
            nodelstarreglos.insertChild(t[2])
    else:
        nodelstarreglos.insertChild(t[1])

    t[0]=nodelstarreglos



#-----------------------------------------------------------------
def p_lstVal(t):
    ''' lstVal  :   lstVal COMA expresionL
                    | expresionL
    '''
    nodelstVal= Node("lstVal")
    if(len(t) == 4):
        nodelstVal.insertChild(t[1])
        nodelstVal.insertChild(Node(","))
        nodelstVal.insertChild(t[3])
    elif(len(t) == 2):
        nodelstVal.insertChild(t[1])
    t[0]=nodelstVal

#-----------------------------------------------------------------
def p_DecStructs(t):
    ''' DecStructs  :   RMUTABLE RSTRUCT ID blockAtributos REND
                        | RSTRUCT ID blockAtributos REND 
    '''
    nodeDecStructs=Node("DecStructs")
    if len(t)==5: #Inmutable        
        nodeDecStructs.insertChild(Node("struct"))
        nodeDecStructs.insertChild(Node(t[2]))
        nodeDecStructs.insertChild(t[3])
        nodeDecStructs.insertChild(Node("end"))
    else: #Mutable
        nodeDecStructs.insertChild(Node("mutable"))
        nodeDecStructs.insertChild(Node("struct"))
        nodeDecStructs.insertChild(Node(t[3]))
        nodeDecStructs.insertChild(t[4])
        nodeDecStructs.insertChild(Node("end"))

    t[0]=nodeDecStructs

#-----------------------------------------------------------------
def p_asignStructs(t):
    ''' asignStructs    :   ID PTO ID IGUAL expresionL
    '''
    nodeasignStructs=Node("asignStructs")
    nodeasignStructs.insertChild(Node(t[1]))
    nodeasignStructs.insertChild(Node("."))
    nodeasignStructs.insertChild(Node(t[3]))
    nodeasignStructs.insertChild(Node("="))
    nodeasignStructs.insertChild(t[5])

    t[0]=nodeasignStructs
#-----------------------------------------------------------------
def p_blockAtributos(t):
    ''' blockAtributos  :   blockAtributos  blockAtributo
                            | blockAtributo
    '''
    nodeblockAtributos=Node("blockAtributos")
    if(len(t)==3):
        nodeblockAtributos.insertChild(t[1])
        nodeblockAtributos.insertChild(t[2])
    elif (len(t)==2):
        nodeblockAtributos.insertChild(t[1])
    
    t[0]=nodeblockAtributos
        
#-----------------------------------------------------------------
def p_blockAtributo(t):
    ''' blockAtributo   :   ID FPTS Tipo PTCOMA
                            | ID PTCOMA
    '''
    nodeblockAtributo=Node("bockAtributo")
    if len(t)==5:
        nodeblockAtributo.insertChild(Node(t[1]))
        nodeblockAtributo.insertChild(Node("::"))
        nodeblockAtributo.insertChild(t[3])
        nodeblockAtributo.insertChild(Node(";"))
    else:
        nodeblockAtributo.insertChild(Node(t[1]))
        nodeblockAtributo.insertChild(Node(";"))

    t[0]=nodeblockAtributo
        

#-----------------------------------------------------------------
def p_ciclo(t):
    ''' ciclo     :   whileSt
    '''
    nodeciclo= Node("ciclo")
    nodeciclo.insertChild(t[1])
    t[0]=nodeciclo

#-----------------------------------------------------------------
def p_whileSt(t):
    ''' whileSt     :   RWHILE expresionL block REND 
    '''
    nodewhileSt= Node("whileSt")
    nodewhileSt.insertChild(Node("while"))
    nodewhileSt.insertChild(t[2])
    nodewhileSt.insertChild(t[3])
    nodewhileSt.insertChild(Node("end"))
    t[0]=nodewhileSt

#-----------------------------------------------------------------
def p_codndicion(t):
    ''' condicion   :   RIF expresionL block REND
                        | RIF expresionL block RELSE block REND
                        | RIF expresionL block elifList REND
    '''
    nodecondicion=Node("condicion")
    if len(t)==5:
        nodecondicion.insertChild(Node("if"))
        nodecondicion.insertChild(t[2])
        nodecondicion.insertChild(t[3])
        nodecondicion.insertChild(Node("end"))
    elif len(t)==7:
        nodecondicion.insertChild(Node("if"))
        nodecondicion.insertChild(t[2])
        nodecondicion.insertChild(t[3])
        nodecondicion.insertChild(Node("else"))
        nodecondicion.insertChild(t[5])
        nodecondicion.insertChild(Node("end"))      
    elif len(t)==6:
        nodecondicion.insertChild(Node("if"))
        nodecondicion.insertChild(t[2])
        nodecondicion.insertChild(t[3])
        nodecondicion.insertChild(Node("elseif"))
        nodecondicion.insertChild(Node("end")) 
        
    t[0]=nodecondicion
#-----------------------------------------------------------------
def p_elifList(t):
    ''' elifList    :   RELIF expresionL block
                        | RELIF expresionL block RELSE block
                        | RELIF expresionL block elifList
    '''
    nodeelifList=Node("elifList")
    if len(t)==4:
        nodeelifList.insertChild(Node("elseif"))
        nodeelifList.insertChild(t[2])
        nodeelifList.insertChild(t[3])
    elif len(t)==6:
       nodeelifList.insertChild(Node("elseif"))
       nodeelifList.insertChild(t[2])
       nodeelifList.insertChild(t[3])
       nodeelifList.insertChild(Node("else"))
       nodeelifList.insertChild(t[5])
    elif len(t)==5:
        nodeelifList.insertChild(Node("elseif"))
        nodeelifList.insertChild(t[2])
        nodeelifList.insertChild(t[3])
        nodeelifList.insertChild(t[4])      

    t[0]=nodeelifList

#------------------------------------------------------------------
def p_block(t):
    '''block    : instrucciones
    '''
    nodeblock = Node("block")
    nodeblock.insertChild(t[1])
    t[0]=nodeblock
def p_strasnferencia(t):
    '''stransferencia   :   RRETURN expresionL
                            | RRETURN
                            | RBREAK
                            | RCONTINUE
    '''
    nodestransferencia=Node("stransferencia")
    if len(t)==3 and t[1]=='return':
        nodestransferencia.insertChild(Node("return"))
        nodestransferencia.insertChild(t[2])
    elif len(t)==2 and t[1]=='return':
        nodestransferencia.insertChild(Node("return"))
       
    elif t[1]=='break':
        nodestransferencia.insertChild(Node("break"))        
    elif t[1]=='continue':
        nodestransferencia.insertChild(Node("continue"))
       
    t[0]=nodestransferencia

#------------------------------------------------------------------

def p_asignacion(t):
    '''asignacion   :   TipoVarible ID IGUAL expresionL Final
                        | TipoVarible ID
                        | ID IGUAL expresionL Final
    '''
    nodeasignacion= Node("asignacion")
    if len(t)==6:
        nodeasignacion.insertChild(t[1])
        nodeasignacion.insertChild(Node(t[2]))
        nodeasignacion.insertChild(Node("="))
        nodeasignacion.insertChild(t[4])
        nodeasignacion.insertChild(t[5])
        
    elif len(t)==3:         
        nodeasignacion.insertChild(t[1])
        nodeasignacion.insertChild(Node(t[2]))
    else:
        nodeasignacion.insertChild(Node(t[1]))
        nodeasignacion.insertChild(Node("="))
        nodeasignacion.insertChild(t[3])
        nodeasignacion.insertChild(t[4])
            
              # Si es un arreglo

    t[0]=nodeasignacion

def p_TipoVarible(t):
    '''TipoVarible   :  RGLOBAL
                        | RLOCAL
    '''
    
    nodeTipoVariable = Node("TipoVariable")
    if(t[1]=='local'):
        nodeTipoVariable.insertChild(Node("local"))
    else:
        nodeTipoVariable.insertChild(Node("global"))
    
    t[0]=nodeTipoVariable

#------------------------------------------------------------------
def p_lstAsingArrays(t):
    ''' lstAsingArrays  :   lstAsingArrays lstAsingArray
                            | lstAsingArray
    '''
    nodelstAsignArrays=Node("lstAsingArrays")
    if(len(t)==3):
        nodelstAsignArrays.insertChild(t[1])
        nodelstAsignArrays.insertChild(t[2])
        
    elif (len(t)==2):
        nodelstAsignArrays.insertChild(t[1])
    
    t[0]=nodelstAsignArrays
#------------------------------------------------------------------
def p_lstAsignArray(t):
    '''lstAsingArray    :   CORIZQ expresionL CORDER
    '''
    nodelstAsingArray=Node("lstAsignArray")
    nodelstAsingArray.insertChild(Node("["))
    nodelstAsingArray.insertChild(t[2])
    nodelstAsingArray.insertChild(Node("]"))
    t[0]=nodelstAsingArray

#------------------------------------------------------------------


def p_Final(t):
    '''Final    :   FPTS Tipo
                    | empty
    '''
    nodeFinal= Node("Final")
    if len(t)==3:
        nodeFinal.insertChild(Node("::"))
        nodeFinal.insertChild(t[2])
    else:
        nodeFinal.insertChild(Node("empty"))

    t[0]=nodeFinal
#------------------------------------------------------------------
def p_Tipo(t):
    '''Tipo :   RINT
                | RFLOAT
                | RBOOL
                | RCHAR
                | RSTRING   
    '''
    nodeTipo= Node("Tipo")
    if t[1]=='Int64'        : nodeTipo.insertChild(Node("Int64"))
    elif t[1]=='Float64'    : nodeTipo.insertChild(Node("Float64"))
    elif t[1]=='Bool'       : nodeTipo.insertChild(Node("Bool"))
    elif t[1]=='Char'       : nodeTipo.insertChild(Node("Char"))
    elif t[1]=='String'     : nodeTipo.insertChild(Node("String"))
    t[0]=nodeTipo
    
#-----------------------------------------------------------------
def p_impresion(t):
    ''' impresion   :   IPRINT PARIZQ val PARDER 
                        | IPRINTLN PARIZQ val PARDER 
    '''
    nodeimpresion=Node("impresion")
    if t[1] =='print'       : 
        nodeimpresion.insertChild(Node("print"))
        nodeimpresion.insertChild(Node("("))
        nodeimpresion.insertChild(t[3])
        nodeimpresion.insertChild(Node(")"))
    elif t[1]=='println'    :
        nodeimpresion.insertChild(Node("println"))
        nodeimpresion.insertChild(Node("("))
        nodeimpresion.insertChild(t[3])
        nodeimpresion.insertChild(Node(")"))

    t[0]=nodeimpresion
#-----------------------------------------------------------------
def p_val(t):
    ''' val     :   val COMA val   
                    | expresionL   
                    
                       
    '''
    nodeval= Node("val")
    if len(t)==2: 
        nodeval.insertChild(t[1])

    elif len(t)==4 and t[2]==',': 
        nodeval.insertChild(t[1])
        nodeval.insertChild(Node(","))
        nodeval.insertChild(t[3])
    
    t[0]=nodeval

#-----------------------------------------------------------------
def p_expresion_logica(t):
    '''expresionL : expresionL AND expresionL
                  | expresionL OR expresionL
                  | NOT expresionL
                  | PARIZQ expresionL PARDER
                  | expresionR
    '''
    nodeexpresionL=Node("expresionL")
    if len(t)==4:
        if t[2] == '&&'  :
            nodeexpresionL.insertChild(t[1])
            nodeexpresionL.insertChild(Node("&&"))
            nodeexpresionL.insertChild(t[3])
        elif t[2] == '||': 
            nodeexpresionL.insertChild(t[1])
            nodeexpresionL.insertChild(Node("||"))
            nodeexpresionL.insertChild(t[3])        
        elif t[1] == '(': t[0]=t[2]
    elif len(t)==3:
        nodeexpresionL.insertChild(Node("!"))
        nodeexpresionL.insertChild(t[2])
    elif len(t)==2:
        nodeexpresionL.insertChild(t[1])

    t[0]=nodeexpresionL
    
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
    nodeexpresionR=Node("expresionR")
    if len(t)==4:
        if t[2] == '>'  :
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node(">"))
            nodeexpresionR.insertChild(t[3])
        elif t[2] == '<':
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node("<"))
            nodeexpresionR.insertChild(t[3])        
        elif t[2] == '>=': 
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node(">="))
            nodeexpresionR.insertChild(t[3])
        elif t[2] == '<=': 
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node("<="))
            nodeexpresionR.insertChild(t[3])   
        elif t[2] == '==':
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node("=="))
            nodeexpresionR.insertChild(t[3])    
        elif t[2] == '!=': 
            nodeexpresionR.insertChild(t[1])
            nodeexpresionR.insertChild(Node("!="))
            nodeexpresionR.insertChild(t[3])
        elif t[1] == '(': 
            nodeexpresionR.insertChild(Node("("))
            nodeexpresionR.insertChild(t[2])
            nodeexpresionR.insertChild(Node(")"))
    elif len(t)==2:
        nodeexpresionR.insertChild(t[1])
    
    t[0]=nodeexpresionR
    
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
    nodeexpresion=Node("expresion")
    if len(t)==4:
        if t[2] == '+'  :
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("+"))
            nodeexpresion.insertChild(t[3])
        elif t[2] == '-': 
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("-"))
            nodeexpresion.insertChild(t[3])
        elif t[2] == '/':
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("/"))
            nodeexpresion.insertChild(t[3])
        elif t[2] == '*': 
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("*"))
            nodeexpresion.insertChild(t[3])
        elif t[2] == '^': 
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("^"))
            nodeexpresion.insertChild(t[3])
        elif t[2] == '%': 
            nodeexpresion.insertChild(t[1])
            nodeexpresion.insertChild(Node("%"))
            nodeexpresion.insertChild(t[3])         
        elif t[1] == '(': 
            nodeexpresion.insertChild(Node("("))
            nodeexpresion.insertChild(t[2])
            nodeexpresion.insertChild(Node(")"))
    elif t[1]=='-':
        nodeexpresion.insertChild(Node("-"))
        nodeexpresion.insertChild(t[2])     
    elif len(t)==2:        
        nodeexpresion.insertChild(t[1])
    
    t[0]=nodeexpresion
#------------------------------------------------------------------

def p_booleano(t):
    ''' booleano    :   VERDADERO
                        | FALSO
    '''
    nodebooleano=Node("booleano")
    nodebooleano.insertChild(Node(t[1]))
    t[0]=nodebooleano

def p_valor_entero(t):
    '''valor    : ENTERO
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    t[0]=nodeovalor


def p_valor_decimal(t):
    '''valor    : DECIMAL
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    t[0]=nodeovalor

def p_valor_char(t):
    '''valor    : CHAR
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    t[0]=nodeovalor

def p_valor_string(t):
    '''valor   :    cadena                   
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(t[1])
    t[0]=nodeovalor

def p_valor_nativas(t):
    '''valor    :   nativas
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(t[1])
    t[0]=nodeovalor

def p_valor_Id (t):
    '''valor    : ID
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    t[0]=nodeovalor

def p_valor_Struct (t):
    '''valor    : ID PTO ID
    '''
    
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    nodeovalor.insertChild(Node("."))
    nodeovalor.insertChild(Node(t[3]))
    t[0]=nodeovalor

def p_valor_funcion(t):
    ''' valor   : callFunc
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(t[1])
    t[0]=nodeovalor

def p_valor_arreglo(t):
    ''' valor   : ID lstAsingArrays  
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node(t[1]))
    nodeovalor.insertChild(t[2])
    t[0]=nodeovalor

def p_valor_Vacio(t):
    ''' valor   : RNOTHING
    '''
    nodeovalor=Node("valor")
    nodeovalor.insertChild(Node("nothing"))
    t[0]=nodeovalor

def p_valor_length(t):
    ''' valor   :   RLENGTH PARIZQ ID PARDER
                |   RLENGTH PARIZQ ID lstAsingArrays PARDER
    '''
    nodevalor= Node("valor")
    if len(t)==5:
        nodevalor.insertChild(Node("lenght"))
        nodevalor.insertChild(Node("("))
        nodevalor.insertChild(Node(t[3]))
        nodevalor.insertChild(Node(")"))        
    else:
        nodevalor.insertChild(Node("lenght"))
        nodevalor.insertChild(Node("("))
        nodevalor.insertChild(Node(t[3]))
        nodevalor.insertChild(t[4])
        nodevalor.insertChild(Node(")")) 

    t[0]=nodevalor

def p_empty(t):
     'empty :'
     nodeempty=Node("empty")
     t[0]=nodeempty
    
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
    nodonativas=Node("nativas")
    if len(t)==5:
        if t[1]=='log10':
            nodonativas.insertChild(Node("log10"))
            nodonativas.insertChild(Node("("))
            nodonativas.insertChild(t[3])
            nodonativas.insertChild(Node(")"))
        elif t[1]=='sin':
            nodonativas.insertChild(Node("sin"))
            nodonativas.insertChild(Node("("))
            nodonativas.insertChild(t[3])
            nodonativas.insertChild(Node(")"))
        elif t[1]=='cos': 
            nodonativas.insertChild(Node("cos"))
            nodonativas.insertChild(Node("("))
            nodonativas.insertChild(t[3])
            nodonativas.insertChild(Node(")"))
        elif t[1]=='tan': 
            nodonativas.insertChild(Node("tan"))
            nodonativas.insertChild(Node("("))
            nodonativas.insertChild(t[3])
            nodonativas.insertChild(Node(")"))
        elif t[1]=='sqrt': 
            nodonativas.insertChild(Node("sqrt"))
            nodonativas.insertChild(Node("("))
            nodonativas.insertChild(t[3])
            nodonativas.insertChild(Node(")"))
    elif len(t)==7:
        nodonativas.insertChild(Node("log"))
        nodonativas.insertChild(Node("("))
        nodonativas.insertChild(t[3])
        nodonativas.insertChild(Node(","))
        nodonativas.insertChild(t[5])
        nodonativas.insertChild(Node(")"))
    elif len(t)==2:
        nodonativas.insertChild(t[1])

    t[0]=nodonativas
        
#--------------------------------------------------------------------
def p_casteo(t):
    '''casteo   :   IPARSE PARIZQ Tipo COMA expresionL PARDER
                    | RTRUNC PARIZQ RINT COMA expresionL PARDER
                    | RTYPEOF PARIZQ expresionL PARDER                    
                    | ISTRING PARIZQ expresionL PARDER
                    | RFLOATC PARIZQ expresionL PARDER
    '''
    nodecasteo=Node("casteo")
    if len(t)==7:
        if t[1]=='parse': 
            nodecasteo.insertChild(Node("parse"))
            nodecasteo.insertChild(Node("("))
            nodecasteo.insertChild(t[3])
            nodecasteo.insertChild(Node(";"))
            nodecasteo.insertChild(t[5])
            nodecasteo.insertChild(Node(")"))
        elif t[1]=='trunc': 
            nodecasteo.insertChild(Node("trunc"))
            nodecasteo.insertChild(Node("("))
            nodecasteo.insertChild(Node("Int64"))
            nodecasteo.insertChild(Node(","))
            nodecasteo.insertChild(t[5])
            nodecasteo.insertChild(Node(")"))
    elif len(t)==5:
        if t[1]=='typeof': 
            nodecasteo.insertChild(Node("typeof"))
            nodecasteo.insertChild(Node("("))
            nodecasteo.insertChild(t[3])
            nodecasteo.insertChild(Node(")"))
        elif t[1]=='string': 
            nodecasteo.insertChild(Node("string"))
            nodecasteo.insertChild(Node("("))
            nodecasteo.insertChild(t[3])
            nodecasteo.insertChild(Node(")"))
        elif t[1]=='float': 
            nodecasteo.insertChild(Node("float"))
            nodecasteo.insertChild(Node("("))
            nodecasteo.insertChild(t[3])
            nodecasteo.insertChild(Node(")"))

    t[0]=nodecasteo
#--------------------------------------------------------------------
def p_cadena(t):
    '''cadena   :   IUPPERCASE PARIZQ expresion PARDER
                    | ILOWERCASE PARIZQ expresion PARDER
                    | IPARSE PARIZQ ISTRING COMA expresionL PARDER
                    | STRING
    '''
    nodecadena=Node("cadena")
    if len(t)==5:
        if t[1]=='uppercase': 
            nodecadena.insertChild(Node("uppercase"))
            nodecadena.insertChild(Node("("))
            nodecadena.insertChild(t[3])
            nodecadena.insertChild(Node(")"))
        elif t[1]=='lowercase': 
            nodecadena.insertChild(Node("lowercase"))
            nodecadena.insertChild(Node("("))
            nodecadena.insertChild(t[3])
            nodecadena.insertChild(Node(")"))
    elif len(t)==7:
        nodecadena.insertChild(Node("parse"))
        nodecadena.insertChild(Node("("))
        nodecadena.insertChild(Node("string"))
        nodecadena.insertChild(Node(","))
        nodecadena.insertChild(t[5])
        nodecadena.insertChild(Node(")"))
    elif len(t)==2: 
        nodecadena.insertChild(Node(t[1]))

    t[0]=nodecadena

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    
    


import ply.yacc as yacc
parser = yacc.yacc()

def Ast(Entrada):
    parser.parse(Entrada)