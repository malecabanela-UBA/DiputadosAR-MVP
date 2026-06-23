# main.py
# Este es el punto de entrada de nuestra API.
# Acá "armamos" la aplicación juntando todos los routers.

from fastapi import FastAPI
from database import crear_tablas
from rutas_auth import router as router_auth
from rutas_votaciones import router as router_votaciones

# -----------------------------------------------------------
# CREAR LA APLICACIÓN
# -----------------------------------------------------------
app = FastAPI(
    title="API de Votaciones Legislativas 🇦🇷",
    description="Predice el voto de diputados usando Machine Learning",
    version="1.0"
)

# -----------------------------------------------------------
# REGISTRAR LOS ROUTERS
# Cada router agrupa un conjunto de endpoints relacionados
# -----------------------------------------------------------
app.include_router(router_auth)          # /auth/registrar y /auth/login
app.include_router(router_votaciones)    # /votaciones/ y /votaciones/predecir


# -----------------------------------------------------------
# EVENTO DE INICIO
# Esto se ejecuta una sola vez cuando arranca la API
# -----------------------------------------------------------
@app.on_event("startup")
def al_iniciar():
    """Crea las tablas en la base de datos si no existen"""
    crear_tablas()
    print("🚀 API iniciada correctamente")


# -----------------------------------------------------------
# ENDPOINT RAÍZ (para verificar que la API está viva)
# -----------------------------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de Votaciones Legislativas 🇦🇷"}


# -----------------------------------------------------------
# PARA CORRER LOCALMENTE:
# uvicorn main:app --reload
#
# Después entrar a: http://127.0.0.1:8000/docs
# Ahí van a ver todos los endpoints documentados automáticamente
# -----------------------------------------------------------
