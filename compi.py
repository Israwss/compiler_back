#Es la Expresion constante
import ply.yacc as yacc
import ply.lex as lex
import time
palabrasClave = ["else","return","str","float","if","while","int"] #Palabras reservadas en C

#Expression de llevara el control de retornos
bloque = []
 
#Almacena el control del programa para imprimir, es un buffer 
EPrograma = []

Expresiones = []

#Detectar el error
ERROR = []

#Acumulador
Acumulador = []

#LISTA DE SIMBOLOS {  identificador : [tipo de dato]}
ListaSimbolos={}

ListaSimbolosG = {}

#LISTA DE FUNCIONES { identificador : tipo que devuelve}
ListaFunciones ={}
			
tokens = [
    # Literals (identifier, integer constant, float constant, string constant, char const)
    'ID', 'INTEGER', 'FLOAT', 'STR',

    # Operators (+,-,*,/,%,|,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=)
    'EQUALS',

    # Increment/decrement (++,--)
    'INCREMENT', 'DECREMENT',

    # Delimiters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMI',

] + palabrasClave

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators
t_EQUALS           = r'='

# Increment/decrement
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

# ?

# Delimiters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_SEMI             = r';'

# String literal
t_STR = r'\"([^\"]*)\"'

# Character constant 'c' or L'c'
#t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in palabrasClave:
        t.type =t.value  # Cambia el tipo si es una palabra clave ya que se debe quedar 
    return t

def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INTEGER(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Definimos cada regla de la gramática en forma de función para PLY.
# La función `p_<NoTerminal>` define cada producción y usa la sintaxis PLY para especificar las reglas.

def p_S(p):
	'''S : program '''
	global EPrograma, Expresiones
	p[0] = (EPrograma,Expresiones)
	EPrograma = []
	Expresiones = []
	
def p_program(p):
	'''program : external_declaration
	| program external_declaration'''
	pass

def p_external_declarationFuncion(p):
	'''external_declaration : function_definition'''
	pass

def p_external_declarationDeclaration(p):
	'''external_declaration : declaration'''	
	global EPrograma
	EPrograma = EPrograma + p[1]
##
def p_function_definition(p):
	'''function_definition : type_specifier ID LPAREN RPAREN compound_statement'''
	global EPrograma, ListaParametros, bloque
	EPrograma= EPrograma + [("#",p[2])] + p[5]                    
	ListaFunciones[p[2]] = (p[1])
	for i in bloque: #Verificamos que todos los return tenga el mismo valor de devolucion
		if i != p[1]:
			ERROR.append(f"{p[2]} se esperaba un {p[1]} y se recibio {i}")
	bloque = []

def p_declaration(p): #Declaration
	'''declaration : init_declarator_list SEMI'''
	p[0] = [p[1]]


def p_init_declarator_list(p): #Voy metiendo los identificadores a la tabla de simbolos
	'''init_declarator_list : type_specifier init_declarator''' 
	if ListaSimbolos[p[2]][0] == None: ListaSimbolos[p[2]][0] = p[1]
	else:  
		t = ListaSimbolos[p[2]][0]
		if ((p[1] == "float") and (t != "str")):
			ListaSimbolos[p[2]][0] = p[1]
		elif (t != p[1]):
			ERROR.append(f"Error de asignacion, no es del tipo")
	p[0] = p[2]
	

def p_type_specifier(p):
	'''type_specifier : int
	| float
	| str'''
	p[0] = p[1]


def p_init_declarator(p): #Ahora guardo el valor, si es que se inicializa.
	'''init_declarator : declarator
	| declarator EQUALS initializer'''
	global Acumulador, Expresiones
	if len(p) == 2: Expresiones.append([0])
	else: ListaSimbolos[p[1]][0] = p[3]
	p[0] = p[1]
	

def p_declarator(p): #Que pasa si desde aqui meto los valores a la tabla donde, el ID es la llave, sino se modifica 'ID', entonces
	'''declarator : ID'''
	ListaSimbolos[p[1]] =[None]
	p[0] = p[1]    
    
    
#No acepta inicializacion de arreglos
def p_initializer(p):
	'''initializer : assignment_expression '''
	global Acumulador
	p[0] = p[1]
	Expresiones.append(Acumulador)
	Acumulador = []
    
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2: p[0] = p[1]
    else: p[0] = p[1] + p[2]

def p_statement(p):
	'''statement : expression_statement
	| declaration	
	| compound_statement
	| selection_statement
	| iteration_statement
	| jump_statement'''
	p[0] = p[1]
	


def p_expression_statement(p):
	'''expression_statement : expression SEMI'''
	p[0] = [p[1]]
	

def p_compound_statement(p):
	'''compound_statement : LBRACE statement_list RBRACE
	| LBRACE  RBRACE''' 
	if len(p) == 4: p[0] = p[2] + ["/"]
	else: p[0] = ["/"]
	 	

def p_selection_statement(p):
	'''selection_statement : if LPAREN expression RPAREN compound_statement
	| if LPAREN expression RPAREN compound_statement else compound_statement'''
	if not (p[3] == "int" or p[3] == "float"): ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico, no acepta expresion con cadenas")
	if len(p)== 6: p[0] = ["$"] + p[5]
	else: p[0] = ["+"] + p[5] + p[7] 	
	
def p_iteration_statement(p):
	'''iteration_statement : while LPAREN expression RPAREN compound_statement'''
	if not (p[3] == "int" or p[3] == "float"): ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico, no acepta expresion con cadenas")
	p[0] = ["&"] + p[5]
	
    
def p_jump_statement(p):
	'''jump_statement : return expression SEMI'''
	if not (p[2] == "int" or p[2] == "float"): ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico, no acepta expresion con cadenasJAJA")
	bloque.append(p[2])
	p[0] = ["?"]

def p_expression(p):
	'''expression : assignment_expression'''
	global Acumulador
	Expresiones.append(Acumulador)
	Acumulador = []
	p[0] = p[1]

def p_assignment_expressionConstante(p):
	'''assignment_expression : conditional_expression '''
	p[0] = p[1]

def p_assignment_expression(p): #Aqui se debe verificar que unary es un id previamente creado en la tabla de simbolos
	'''assignment_expression : ID EQUALS assignment_expression'''
	if (p[1] not in ListaSimbolos): 
		ERROR.append(f"Error semantico, no se encuentra dicho id: {p[1]} ")
	elif ((ListaSimbolos[p[1]][0] == "float") and (p[3] != "str")):
			p[0] = p[1]
	elif (p[3] != ListaSimbolos[p[1]][0]):
		ERROR.append(f"Error semantico, asignacion de diferente tipo")
	p[0] = p[1]

#Yo solo voy a verificar que se ha diferente de 0
def p_conditional_expression(p):
	'''conditional_expression : logical_or_expression'''
	p[0] = p[1]
	
def p_logical_or_expression(p):
	'''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression'''
	global Acumulador
	if (len(p)==2): p[0] = p[1]
	else:
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta comparacion cadenas0")
		Acumulador.append(",")
		p[0] = "int"
	
def p_logical_and_expression(p):
	'''logical_and_expression : equality_expression
	| logical_and_expression LAND equality_expression'''
	global Acumulador
	if (len(p)==2): p[0] = p[1]
	else:
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta comparacion cadenas0")
		Acumulador.append("$")
		p[0] = "int"
		
def p_equality_expression(p):
	'''equality_expression : relational_expression
	| equality_expression EQ relational_expression
	| equality_expression NE relational_expression'''
	global Acumulador
	if len(p) == 2 : p[0] = p[1]	
	else:	
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta comparacion cadenas0")
		if (p[2] == '=='): Acumulador.append("#") 
		elif (p[2] == '!='): Acumulador.append("&")
		p[0] = "int" 
		
		
def p_relational_expression(p):
	'''relational_expression : additive_expression
	| relational_expression LT additive_expression
	| relational_expression GT additive_expression
	| relational_expression LE additive_expression
	| relational_expression GE additive_expression'''
	global Acumulador
	if len(p) == 2 : p[0] = p[1]	
	else:	
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta comparacion cadenas0")
		if (p[2] == '<'): Acumulador.append("<") 
		elif (p[2] == '>'): Acumulador.append(">") 
		elif (p[2] == '<='): Acumulador.append("]")
		elif (p[2] == '>='): Acumulador.append("[") 
		p[0] = "int"
		
def p_additive_expression(p):
	'''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression'''
	global Acumulador
	if len(p) == 2 : p[0] = p[1]	
	else:	
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta operacion con cadenas0")
		if (p[2] == '+'): Acumulador.append("+")
		elif (p[2] == '-'): Acumulador.append("-")
		if (p[1] != p[3]): p[0] = "float"
		else: p[0] = p[1]

def p_multiplicative_expression(p):
	'''multiplicative_expression : unary_expression
	| multiplicative_expression TIMES unary_expression
	| multiplicative_expression DIVIDE unary_expression'''
	global Acumulador
	if len(p) == 2 : p[0] = p[1]	
	else:	
		if not ((p[1] == "int" or p[1] == "float") and (p[3] == "int" or p[3] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta operacion con cadenas1")
		if (p[2] == '*'): Acumulador.append("*")
		elif (p[2] == '/'): Acumulador.append("/")
		if (p[1] != p[3]): p[0] = "float"
		else: p[0] = p[1]
	
def p_unary_expression(p):
	'''unary_expression : postfix_expression
	| LNOT unary_expression
	| MINUS unary_expression
	| INCREMENT unary_expression
	| DECREMENT unary_expression'''
	if len(p) == 2: p[0] = p[1]
	else: 
		if not ((p[2] == "int" or p[2] == "float")): 
			ERROR.append(f"Error en la linea: {p.lineno(1)},Error Semantico,no acepta operacion con cadenas1")
		p[0] = p[2]

def p_postfix_expression(p): 
	'''postfix_expression : primary_expression'''
	p[0] = p[1]

def p_postfix_Expression_Funciones(p):
	''' postfix_expression : ID LPAREN  RPAREN'''
	global Acumulador
	if(p[1] not in ListaFunciones): 
		ERROR.append(f"Definir primero la funcion : {p[1]}")
	else: 
		Acumulador.append([p[1]])
		p[0] = ListaFunciones[p[1]]
####

def p_primary_expression_ID(p):
	'''primary_expression : ID '''
	global Acumulador
	if (p[1] not in ListaSimbolos): 
		ERROR.append(f"Error en la linea: {p.lineno(1)} Declara primero el id : {p[1]}")
	else: p[0] = ListaSimbolos[p[1]][0]
	Acumulador.append(p[1])
	
	
def p_primary_expression(p):
	'''primary_expression : INTEGER
	| FLOAT
	| STR
	| LPAREN logical_or_expression RPAREN'''
	global Acumulador
	if (len(p) == 2 ): 
		p[0] = type(p[1]).__name__
		Acumulador.append(p[1])
	else:
		p[0] = p[2]

	
    
# Error rule for syntax errors
def p_error(p):
	if p:
		print(f"Error de sintaxis en la línea {p.lineno}, algo falta antes de {p.value}")
		raise ValueError("Error de sintaxis")
	else:
		print(f"Error de sintaxis al final de la entrada")
		raise ValueError("Error de sintaxis")


#Puedo guardar en las sentencias el nombre de asignacion de la variable, es decir, en vez de A, guarde i y k
def Pruebas(s):
    """Ejecuta el análisis del código fuente y retorna el resultado."""
    global ERROR, ListaSimbolos, ListaFunciones, EPrograma, Expresiones, bloque

    # Reinicia las variables globales
    ERROR = []
    ListaSimbolos = {}
    ListaFunciones = {}
    EPrograma = []
    Expresiones = []
    bloque = []

    result = parser.parse(s)
    response = {
        "syntax_passed": True,
        "semantic_errors": [],
        "symbols": ListaSimbolos,
        "functions": ListaFunciones,
        "parsed_program": None,
    }

    if ERROR:
        response["semantic_errors"] = ERROR
        ERROR = []
    if result:
        response["parsed_program"] = result
    return response


lexer = lex.lex()
parser = yacc.yacc()


