from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os, sys
p = os.path.abspath(".")
sys.path.insert(1, p)

app = FastAPI(title="CRUD de Personas sin Base de Datos")

# Lista en memoria para almacenar los datos de las personas
personas = []

# Modelo de entrada de datos para una persona
class PersonaBase(BaseModel):
    nombre: str = Field(..., example="Juan Pérez")
    edad: int = Field(..., ge=0, example=30)
    telefono: str = Field(..., example="1234567890")

# Modelo para crear una nueva persona (misma estructura que PersonaBase)
class PersonaCreate(PersonaBase):
    pass

# Modelo para actualizar una persona (permitimos campos opcionales)
class PersonaUpdate(BaseModel):
    nombre: str | None = Field(None, example="Juan Pérez")
    edad: int | None = Field(None, ge=0, example=31)
    telefono: str | None = Field(None, example="0987654321")

# Modelo para mostrar una persona con su ID
class PersonaResponse(PersonaBase):
    id: int

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:5000",  # Dirección de la aplicación Flask
    # Agrega más orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para crear una nueva persona
@app.post("/personas/", response_model=PersonaResponse, status_code=201)
def crear_persona(persona: PersonaCreate):
    # Verificamos si el número de teléfono ya existe en la lista
    for p in personas:
        if p['telefono'] == persona.telefono:
            raise HTTPException(status_code=400, detail="El número de teléfono ya está registrado.")
    
    # Asignamos un ID automático basado en la longitud de la lista
    nueva_persona = {
        "id": len(personas) + 1,
        "nombre": persona.nombre,
        "edad": persona.edad,
        "telefono": persona.telefono
    }
    personas.append(nueva_persona)
    return nueva_persona

# Ruta para obtener todas las personas
@app.get("/personas/", response_model=List[PersonaResponse])
def obtener_personas():
    return personas

# Ruta para obtener una persona por su ID
@app.get("/personas/{persona_id}", response_model=PersonaResponse)
def obtener_persona(persona_id: int):
    for persona in personas:
        if persona['id'] == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada.")

# Ruta para actualizar una persona
@app.put("/personas/{persona_id}", response_model=PersonaResponse)
def actualizar_persona(persona_id: int, persona_actualizada: PersonaUpdate):
    for persona in personas:
        if persona['id'] == persona_id:
            if persona_actualizada.nombre is not None:
                persona['nombre'] = persona_actualizada.nombre
            if persona_actualizada.edad is not None:
                persona['edad'] = persona_actualizada.edad
            if persona_actualizada.telefono is not None:
                # Verificar si el nuevo número de teléfono ya existe en otra persona
                for p in personas:
                    if p['telefono'] == persona_actualizada.telefono and p['id'] != persona_id:
                        raise HTTPException(status_code=400, detail="El número de teléfono ya está registrado.")
                persona['telefono'] = persona_actualizada.telefono
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada.")

# Ruta para eliminar una persona
@app.delete("/personas/{persona_id}", status_code=204)
def eliminar_persona(persona_id: int):
    for i, persona in enumerate(personas):
        if persona['id'] == persona_id:
            personas.pop(i)
            return
    raise HTTPException(status_code=404, detail="Persona no encontrada.")
