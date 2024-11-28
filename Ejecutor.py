#Clasifico la entrada:  asignacion= "A", etiqueta = "E", validacion = "V", goto = "G", retorno(Quitar en pila) = "R", llamada(Meter en pila) = "L", meter valor retorno = "U", sacar valor retorno = "O" 

#Recibo: Asignacion "A"= [sentencia, operacion, operando1,operando2,resultado] 
#Recibo Etiqueta "E" = pass
#Recibo validacion "V" = [sentencia, operacion,operando1,operando2,resultado]
#Recibo goto "G" = saltar a esa linea marcada, como la direccion de la etiqueta que esta en el diccionario.
#Recibo retorno "R" = Se obtiene los parametros metidos en la pila y se obtiene la ultima direccion leida
#Recibo llamada "L" = Significa que metemos los paramtros en la pila y se guarda la ultima direccion leida.  
#Recibo meter valor a pila "U" = cuando se pasan como parametros ciertos valores primero se meten a pila antes de llamar a la funcion
#Recibo sacar valor de pila "0" = cundo se obtienen los valores de la pila
# #,funcion2,?,/,#,main,kola,a,$,a,/,+,a,/,a,/,&,a,/,/

#Todas las variables creadas o identificadores seran guardados y tratadas de igual manera, ya que al final y al cabo son 


#Pila del programa PrincipalpOR = [funcion(1),parametros1, funcion(2),parametros2,...]

#Variables de programa, ya me las da la lista del programa que tiene la lista de variables

Variables = {}

#Funciones del programa funciones = {"nombreFuncion": localidadEn etiqueta}



#ALU: Realizara todas las operaciones aritmeticas y logicas, se adjudica que nuestra alu puede hacer comparaciones complejas y compuestas
# los muchos if representan un multiplexor

def ALU(op,opr1,opr2):
	if op == "+": return opr1 + opr2
	elif op == "-": return 	opr1 - opr2
	elif op == "*": return 	opr1 * opr2
	elif op == "/": return 	opr1 / opr2
	elif op == "<": return 	1 if opr1 < opr2 else 0
	elif op == ">": return 	1 if opr1 > opr2 else 0
	elif op == "]": return 1 if opr1 <= opr2 else 0
	elif op == "[": return 1 if opr1 >= opr2 else 0
	elif op == "#": return 1 if opr1 == opr2 else 0
	elif op == "&": return 1 if opr1 != opr2 else 0
	return opr1

def SecuenciaPrograma(Programa, etiquetas):
	PrincipalpOP = []
	PilaRetornoArgumentos = []
	if etiquetas.get("main") == None: 
		print("No se encontro la funcion main")
		return 
	i = etiquetas["main"]
	PrincipalpOP.append(i)
	while PrincipalpOP:
		if Programa[i][0] == "A": 
			l = Variables[Programa[i][2]] if Programa[i][2] in Variables else Programa[i][2]
			k = Variables[Programa[i][3]] if Programa[i][3] in Variables else Programa[i][3]
			Variables[Programa[i][4]] = ALU(Programa[i][1],l,k) 
		elif Programa[i][0] == "V": 
			l = Variables[Programa[i][2]] if Programa[i][2] in Variables else Programa[i][2]
			k = Variables[Programa[i][3]] if Programa[i][3] in Variables else Programa[i][3]
			i = (etiquetas[Programa[i][4]]-1) if ALU(Programa[i][1],l,k) else i 
		elif Programa[i][0] == "G": i = etiquetas[Programa[i][1]] - 1
		elif Programa[i][0] == "O": Variables[Programa[i][1]] = PilaRetornoArgumentos.pop()
		elif Programa[i][0] == "U": PilaRetornoArgumentos.append(Variables[Programa[i][1]])
		elif Programa[i][0] == "L": 
			PrincipalpOP.append(i)
			i = etiquetas[Programa[i][1]]
		elif Programa[i][0] == "R": i = PrincipalpOP.pop()
		#print(f"linea: {i} Variables: {Variables} Pila: {PrincipalpOP}")
		#input("pausa")
		i = i + 1  
	print("Modificacion Variables Despues de correr:")
	print(Variables)	
	
	
