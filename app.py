from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para una receta
class Receta(BaseModel):
    nombre: str
    descripcion: str
    ingredientes: List[str]

# Base de datos simulada en memoria
recetas = [
    {"id": 1, "nombre": "Pizza Margarita", "descripcion": "Una pizza clásica italiana.", "ingredientes": ["Masa", "Salsa de tomate", "Mozzarella"]},
    {"id": 2, "nombre": "Ensalada César", "descripcion": "Una ensalada fresca y crujiente.", "ingredientes": ["Lechuga", "Pollo", "Queso parmesano", "Aderezo César"]}
]

# 0. Página de inicio
@app.get("/")
async def inicio():
    return {"mensaje": "Bienvenido a la API de Recetas de Comida"}

# 1. Obtener todas las recetas
@app.get("/recetas", response_model=List[dict])
async def obtener_recetas():
    return recetas

# 2. Obtener una receta por ID
@app.get("/recetas/{id}", response_model=dict)
async def obtener_receta(id: int):
    receta = next((r for r in recetas if r["id"] == id), None)
    if receta:
        return receta
    raise HTTPException(status_code=404, detail="Receta no encontrada")

# 3. Crear una nueva receta
@app.post("/recetas", response_model=dict)
async def crear_receta(receta: Receta):
    nueva_receta = {
        "id": len(recetas) + 1,
        "nombre": receta.nombre,
        "descripcion": receta.descripcion,
        "ingredientes": receta.ingredientes
    }
    recetas.append(nueva_receta)
    return nueva_receta

# 4. Actualizar una receta existente
@app.put("/recetas/{id}", response_model=dict)
async def actualizar_receta(id: int, receta: Receta):
    for r in recetas:
        if r["id"] == id:
            r["nombre"] = receta.nombre
            r["descripcion"] = receta.descripcion
            r["ingredientes"] = receta.ingredientes
            return r
    raise HTTPException(status_code=404, detail="Receta no encontrada")

# 5. Eliminar una receta
@app.delete("/recetas/{id}", response_model=dict)
async def eliminar_receta(id: int):
    global recetas
    receta_eliminada = next((r for r in recetas if r["id"] == id), None)
    if receta_eliminada:
        recetas = [r for r in recetas if r["id"] != id]
        return {"mensaje": "Receta eliminada"}
    raise HTTPException(status_code=404, detail="Receta no encontrada")

