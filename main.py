from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import compi
import Ejecutor   
import principal 

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# Clase para manejar el input
class CodeRequest(BaseModel):
    code: str

@app.post("/compile/")
async def compile_code(request: CodeRequest):
    try:
        # Llama al compilador
        compile_result = compi.Pruebas(request.code)

        # Verifica si el análisis sintáctico pasó
        if not compile_result.get("syntax_passed", False):
            return {
                "status": "error",
                "message": "Análisis sintáctico fallido.",
                "details": compile_result,
            }

        # Retorna los detalles del análisis
        return {
            "status": "success",
            "message": "Análisis sintáctico completado.",
            "details": compile_result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la compilación: {str(e)}"
        )


@app.post("/execute/")
async def execute_code(request: CodeRequest):
    try:
        # Realiza el análisis inicial con el compilador
        compile_result = compi.Pruebas(request.code)

        # Verifica si el análisis sintáctico pasó
        if not compile_result.get("syntax_passed", False):
            return {
                "status": "error",
                "message": "Análisis sintáctico fallido.",
                "details": compile_result,
            }

        # Verifica si existe el programa analizado
        parsed_program = compile_result.get("parsed_program")
        if not parsed_program:
            return {
                "status": "error",
                "message": "El programa no fue analizado correctamente.",
                "details": compile_result,
            }

        # Llama al ejecutor para procesar el programa analizado
        program_result = principal.SentidoPrograma(
            parsed_program[0], parsed_program[1]
        )
        print(program_result)

        # Retorna los resultados del análisis y ejecución
        return {
    "status": "success",
    "message": "Ejecución completada con éxito.",
    "details": {
        "compile_result": compile_result,
        "execution_result": program_result,
    },
}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la ejecución: {str(e)}"
        )

