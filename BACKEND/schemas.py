# schemas.py
# Los "schemas" son moldes que le dicen a FastAPI
# qué forma tienen que tener los datos que llegan y los que salen.
# Si alguien manda un dato que no cumple el molde, FastAPI
# rechaza el pedido automáticamente (validación automática).

from pydantic import BaseModel
from typing import Literal


# -----------------------------------------------------------
# SCHEMAS DE USUARIO
# -----------------------------------------------------------

class UsuarioCrear(BaseModel):
    """Lo que necesitamos para crear un usuario nuevo"""
    nombre: str
    contrasena: str


class UsuarioRespuesta(BaseModel):
    """Lo que devolvemos cuando consultamos un usuario (sin la contraseña)"""
    id: int
    nombre: str

    class Config:
        from_attributes = True  # permite convertir objetos SQLAlchemy a este schema


# -----------------------------------------------------------
# SCHEMAS DE VOTACIÓN
# -----------------------------------------------------------

class VotacionCrear(BaseModel):
    """Lo que necesitamos para registrar una votación"""
    diputado: str
    bloque: str
    provincia: str
    tipo_proyecto: str
    voto: Literal["AFIRMATIVO", "NEGATIVO", "ABSTENCION"]  # solo acepta estos tres valores


class VotacionRespuesta(VotacionCrear):
    """Lo que devolvemos cuando consultamos una votación (igual + el id)"""
    id: int

    class Config:
        from_attributes = True


# -----------------------------------------------------------
# SCHEMA DE PREDICCIÓN
# -----------------------------------------------------------

class PrediccionEntrada(BaseModel):
    """Los datos que necesita el modelo para hacer una predicción"""
    bloque: str
    provincia: str
    tipo_proyecto: str


class PrediccionSalida(BaseModel):
    """Lo que devuelve el modelo después de predecir"""
    voto_predicho: str          # AFIRMATIVO, NEGATIVO o ABSTENCION
    confianza: float            # qué tan seguro está el modelo (0 a 1)


# -----------------------------------------------------------
# SCHEMA DE LOGIN
# -----------------------------------------------------------

class LoginDatos(BaseModel):
    """Los datos para iniciar sesión"""
    nombre: str
    contrasena: str


class TokenRespuesta(BaseModel):
    """El token que devolvemos si el login fue exitoso"""
    access_token: str
    token_type: str = "bearer"
