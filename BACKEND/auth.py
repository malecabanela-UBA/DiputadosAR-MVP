# auth.py
# Este archivo maneja dos cosas:
# 1. Encriptar y verificar contraseñas (con bcrypt)
# 2. Crear y verificar tokens JWT (para mantener la sesión)

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# -----------------------------------------------------------
# CONFIGURACIÓN DE CONTRASEÑAS
# bcrypt convierte "1234" en algo como "$2b$12$..."
# así si alguien roba la base de datos, no puede leer las contraseñas
# -----------------------------------------------------------
contexto_encriptacion = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encriptar_contrasena(contrasena: str) -> str:
    """Convierte una contraseña de texto plano en su versión encriptada"""
    return contexto_encriptacion.hash(contrasena)

def verificar_contrasena(contrasena_plana: str, contrasena_encriptada: str) -> bool:
    """Compara una contraseña ingresada con la versión encriptada guardada"""
    return contexto_encriptacion.verify(contrasena_plana, contrasena_encriptada)


# -----------------------------------------------------------
# CONFIGURACIÓN DE JWT
# JWT = JSON Web Token
# Es una "credencial digital" que le damos al usuario al loguearse
# El usuario la manda en cada pedido para demostrar que está autenticado
# -----------------------------------------------------------
CLAVE_SECRETA = "clave-super-secreta-cambiar-en-produccion"  # en producción va en .env
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 60  # el token dura 1 hora

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def crear_token(datos: dict) -> str:
    """
    Crea un token JWT con los datos del usuario.
    El token incluye una fecha de expiración automática.
    """
    datos_token = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION)
    datos_token.update({"exp": expiracion})
    token = jwt.encode(datos_token, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token

def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Verifica que el token sea válido y devuelve el nombre del usuario.
    Se usa como dependencia en los endpoints protegidos.
    """
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado. Por favor volvé a iniciar sesión.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token para leer los datos que contiene
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        nombre_usuario = payload.get("sub")
        if nombre_usuario is None:
            raise error_credenciales
        return nombre_usuario
    except JWTError:
        raise error_credenciales
