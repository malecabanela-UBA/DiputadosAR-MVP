# rutas_votaciones.py
# Acá están los endpoints para trabajar con votaciones:
# - Ver todas las votaciones
# - Agregar una votación nueva
# - Hacer una predicción con el modelo de ML

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import joblib
import pandas as pd
import os

from database import get_db, Votacion
from schemas import VotacionCrear, VotacionRespuesta, PrediccionEntrada, PrediccionSalida
from auth import verificar_token

router = APIRouter(prefix="/votaciones", tags=["Votaciones"])


# -----------------------------------------------------------
# CARGAR EL MODELO AL INICIAR
# El modelo se carga una sola vez en memoria cuando arranca la API
# así no tenemos que cargarlo en cada predicción (sería muy lento)
# -----------------------------------------------------------
RUTA_MODELO = os.path.join(os.path.dirname(__file__), "..", "MODELO", "modelo_votacion.pkl")

modelo = None
if os.path.exists(RUTA_MODELO):
    modelo = joblib.load(RUTA_MODELO)
    print("✅ Modelo cargado correctamente")
else:
    print("⚠️  Modelo no encontrado. El endpoint de predicción no va a funcionar hasta que entrenes el modelo.")


# -----------------------------------------------------------
# ENDPOINTS
# Todos requieren token (usuario logueado) gracias a Depends(verificar_token)
# -----------------------------------------------------------

@router.get("/", response_model=List[VotacionRespuesta])
def ver_votaciones(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(verificar_token)  # solo usuarios logueados
):
    """Devuelve todas las votaciones guardadas en la base de datos"""
    votaciones = db.query(Votacion).all()
    return votaciones


@router.post("/", response_model=VotacionRespuesta)
def agregar_votacion(
    datos: VotacionCrear,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(verificar_token)
):
    """Agrega una votación nueva a la base de datos"""
    nueva_votacion = Votacion(
        diputado=datos.diputado,
        bloque=datos.bloque,
        provincia=datos.provincia,
        tipo_proyecto=datos.tipo_proyecto,
        voto=datos.voto
    )
    db.add(nueva_votacion)
    db.commit()
    db.refresh(nueva_votacion)
    return nueva_votacion


@router.post("/predecir", response_model=PrediccionSalida)
def predecir_voto(
    datos: PrediccionEntrada,
    usuario_actual: str = Depends(verificar_token)
):
    """
    Usa el modelo de Machine Learning para predecir cómo va a votar
    un diputado dado su bloque, provincia y tipo de proyecto.
    """
    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="El modelo no está disponible. Ejecutá primero el script de entrenamiento."
        )

    # Convertimos los datos de entrada en un DataFrame (que es lo que espera el modelo)
    entrada = pd.DataFrame([{
        "bloque": datos.bloque,
        "provincia": datos.provincia,
        "tipo_proyecto": datos.tipo_proyecto
    }])

    # El modelo predice el voto y la probabilidad de cada opción
    voto_predicho = modelo.predict(entrada)[0]
    probabilidades = modelo.predict_proba(entrada)[0]
    confianza = float(max(probabilidades))  # la probabilidad más alta

    return {
        "voto_predicho": voto_predicho,
        "confianza": round(confianza, 2)
    }
