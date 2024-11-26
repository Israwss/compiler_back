#				Unidad  Central  De Procesamiento CPU

#Aunque se puede realizar la ejecucion despues de obtener el postfix, nosotros como equipo decidimos desplegar el 
# TAC y luego hacer la evaluacion de las expresiones desde ahi para simular el comportamiento del sistema de evaluacion de TAC

import compi as compilador #Compilador lo transforma a codigo intermedio(Esta vez planteamos una relacion potsfix y TAC)
import Ejecutor as CU # Unidad de Control
#Control de etiquetas
DireccionEtique = {}

EtiqueNum = 0

look = 0

#Representa el valor en guardado en memoria
Pgro = []

#Operando Reconocibles
Operandos = ["+","-","*","/","<",">","[","]","#","&","$",","]

OpeandosCom = ["<",">","[","]","#","&","$",","]


def Comparaciones(signo,a,b,control):
	global EtiqueNum, look, Pgro
	t = f"t{control}"
	if signo == "$": #&&
		Pgro.append(["A", "=", 0, 0, f"t{control}"])
		print(f"{look}: t{control} = 0") #Se almacena primero un 0
		Pgro.append(["V","#",b,0,f"v{EtiqueNum}"])
		print(f"{look + 1}: if {b} == 0 goto v{EtiqueNum}")#Como es and si sale 0, te vas a la siguiente instruccion no sigues validando
		Pgro.append(["V","#",a,0,f"v{EtiqueNum}"])
		print(f"{look + 2}: if {a} == 0 goto v{EtiqueNum}")
		Pgro.append(["A", "=", 1, 0, f"t{control}"])
		print(f"{look + 3}: t{control} = 1") #Si es 0, te vas a la que sigue de esta
		DireccionEtique[f"v{EtiqueNum}"] = look + 4
		Pgro.append("E")
		print(f"{look + 4}: v{EtiqueNum}: ")
		look = look + 5
		control,EtiqueNum = control + 1, EtiqueNum + 1
		return t
	elif signo == ",": # || 
		Pgro.append(["A", "=", 1, 0, f"t{control}"])
		print(f"{look}: t{control} = 1") #Se almacena primero un 1
		Pgro.append(["V","&",b,0,f"v{EtiqueNum}"])
		print(f"{look + 1} :if {b} != 0 goto v{EtiqueNum}")#Como es or si sale 1(diferente de 0), te vas a la siguiente instruccion no sigues validando
		Pgro.append(["V","&",a,0,f"v{EtiqueNum}"])
		print(f"{look + 2}: if {a} != 0 goto v{EtiqueNum}")
		Pgro.append(["A", "=", 0, 0, f"t{control}"])
		print(f"{look + 3}: t{control} = 0 ") #Si es 1, te vas a la que sigue de esta, pero si ya pasaste ambas y no cumple entonces cambias a0
		DireccionEtique[f"v{EtiqueNum}"] = look + 4
		Pgro.append("E")
		print(f"{look + 4}: v{EtiqueNum}:")
		look = look + 5
		control, EtiqueNum = control + 1, EtiqueNum + 1
		return t
	Pgro.append(["A","=",1,0,f"t{control}"])	
	print(f"{look}: t{control} = 1")
	look = look + 1
	if signo == "<": print(f"{look}: if {b} < {a} goto v{EtiqueNum}")
	elif signo == ">": print(f"{look}: if {b} > {a} goto v{EtiqueNum}")
	elif signo == "]": print(f"{look}: if {b} <=  {a} goto v{EtiqueNum}")
	elif signo == "[": print(f"{look}: if {b} >= {a} goto v{EtiqueNum}")
	elif signo == "#": print(f"{look}: if {b} == {a} goto v{EtiqueNum}")
	elif signo == "&": print(f"{look}: if {b} != {a} goto v{EtiqueNum}")
	Pgro.append(["V",signo,b,a,f"v{EtiqueNum}"])
	look = look + 1
	Pgro.append(["A","=",0,0,f"t{control}"])
	print(f"{look}: t{control} = 0")
	look = look + 1
	DireccionEtique[f"v{EtiqueNum}"] = look
	Pgro.append("E")
	print(f"{look}: v{EtiqueNum}:")
	look = look + 1 
	EtiqueNum = EtiqueNum + 1	
	return t

def Evaluacion(Acumulador):
	global look, Pgro
	primero,control = 0, 0
	pila = []
	if len(Acumulador) == 1:
		l =  Acumulador.pop()
		if isinstance(l, list): 
				Pgro.append(["L", l[0]]) 
				print(f"{look}: CALL {l[0]}")
				Pgro.append(["O", f"t{control}"])
				print(f"{look+1}: POP t{control}")
				pila.append(f"t{control}")
				control,look = control + 1, look + 2
		else:		
			Pgro.append(["A", "=", l, 0, f"t{control}"])
			print(f"{look}: t{control} = {l}") 
			control = control + 1
			look = look + 1
	for i in Acumulador:
		if i in Operandos:
			k = pila.pop()
			l = pila.pop()
			if i in OpeandosCom:
				t = Comparaciones(i,k,l,control) 
				control = control + 1			
				pila.append(t)
				continue
			pila.append(f"t{control}")
			Pgro.append(["A", i, l, k, f"t{control}"]) 
			print(f"{look}: t{control} = {l} {i} {k}")
			look = look + 1
			control = control + 1
		else:
			if isinstance(i, list): 
				Pgro.append(["L", i[0]]) 
				print(f"{look}: CALL {i[0]}")
				Pgro.append(["O", f"t{control}"])
				print(f"{look+1}: POP t{control}")
				pila.append(f"t{control}")
				control,look = control + 1, look + 2
			else:
				pila.append(i)			
	return f"t{control-1}" 

# F -- #;  I -- $;  IE -- +; W -- &; B -- /; 
def SentidoPrograma(Programa,Expresiones):
	global look,DireccionEtique, Pgro
	PilaP = []
	ConEtique= 0
	for sentencia in Programa:
		if sentencia[0] == "#": #Espero recibir ("F",nombreFuncion)
			Pgro.append("E")
			print(f"{look}: {sentencia[1]}: ")
			DireccionEtique[sentencia[1]] = look
			PilaP.append(f"RET")
		elif sentencia == "$":
			jola = Evaluacion(Expresiones.pop(0)) 
			Pgro.append(["V","#",jola,0,f"Etiqueta{ConEtique}"])
			print(f"{look}: if ({jola} == 0) goto Etiqueta{ConEtique}: ")
			PilaP.append(f"Etiqueta{ConEtique}")
			ConEtique = ConEtique + 1
		elif sentencia == "+":
			jola = Evaluacion(Expresiones.pop(0)) 
			Pgro.append(["V","#",jola,0,f"Etiqueta{ConEtique}"])
			print(f"{look}: if ({jola} == 0) goto Etiqueta{ConEtique}")
			PilaP.append(f"Etiqueta{ConEtique+1}")
			PilaP.append((f"Etiqueta{ConEtique+1}",f"Etiqueta{ConEtique}"))
			ConEtique = ConEtique + 2
		elif sentencia == "&":
			Pgro.append("E")
			print(f"{look}: Etiqueta{ConEtique}:")
			DireccionEtique[f"Etiqueta{ConEtique}"] = look
			look = look + 1
			jola =  Evaluacion(Expresiones.pop(0))
			Pgro.append(["V","#",jola,0,f"Etiqueta{ConEtique + 1}"])
			print(f"{look}: if ({jola} == 0) goto Etiqueta{ConEtique + 1}")
			PilaP.append((f"Etiqueta{ConEtique}",f"Etiqueta{ConEtique+1}"))
			ConEtique = ConEtique + 2
		elif sentencia == "?": 
			jola =  Evaluacion(Expresiones.pop(0))
			Pgro.append(["U",jola])
			print(f"{look}: PUSH {jola}")
			Pgro.append("R")
			print(f"{look + 1}: RET")
			look = look + 1
		elif sentencia == "/":	
			t = PilaP.pop()
			if len(t)==2:
				DireccionEtique[t[1]] = look + 1
				Pgro.append(["G",t[0]])
				Pgro.append(["E",t[1]]) 
				print(f"{look}: goto {t[0]}\n{look + 1}: {t[1]}:")
				look = look + 1
			else:
				if t == "RET":
					Pgro.append("R")
				else:
					Pgro.append("E") 
				DireccionEtique[t] = look
				print(f"{look}: {t}:")
		else:
			jola = Evaluacion(Expresiones.pop(0))
			Pgro.append(["A", "=", jola, 0, sentencia]) 
			print(f"{look}: {sentencia} =  {jola}")
		look = look + 1
		

if __name__ == '__main__':
	s = '''
	int funcion2(){
		return 9 + 6;
	}
	int main(){
		float kola; 
		int a = funcion2() + 4;
		if (a < 20){
			a = 9;
		}
		if (a < 10){
			a = 3;
		}
		else {
			a = 40;
		}
		while(a<50){
			a = a + 1;
		}	
	}
'''
#int resultado = (5 + 3 * 2 > 10 && 20 / 4 <= 5) * (15 - 6) + (8 / 2 == 4 || 7 * 3 > 25) * (30 - 12 / 4);
#int resultado = ((10 - 2 * 3 < 5 || 18 / 3 >= 6) && (7 + 5 * 2 != 17)) * (25 - 5 * 3) + (5 * ((14 / 2 == 7 && 4 * 3 > 10) || (30 / 5 <= 6)));
	
#Podemos a guardar los tipos de las variables del return y cuando llegue a la funcion desapilarlos y verificar los tipos de cada uno coincide con los tipos de devolucion al definir 	
	try:
		t = compilador.Pruebas(s)
		#print(t[0])
		#print(t[1])
		SentidoPrograma(t[0],t[1])
		print("Etiquetas: ")
		print(DireccionEtique)
		#print(Pgro)
		CU.SecuenciaPrograma(Pgro,DireccionEtique)
	except Exception as e:
		print("Existe un error: ", e)
