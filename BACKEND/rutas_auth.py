# rutas_auth.py
# Acá definimos los endpoints relacionados con usuarios:
# - Registrar un usuario nuevo
# - Iniciar sesión y obtener un token

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db, Usuario
from schemas import UsuarioCrear, UsuarioRespuesta, LoginDatos, TokenRespuesta
from auth import encriptar_contrasena, verificar_contrasena, crear_token

# El router es como un "sub-aplicación" que agrupa rutas relacionadas
# Todas las rutas acá van a tener el prefijo /auth
router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registrar", response_model=UsuarioRespuesta)
def registrar_usuario(datos: UsuarioCrear, db: Session = Depends(get_db)):
    """
    Crea un usuario nuevo en la base de datos.
    La contraseña se guarda encriptada, nunca en texto plano.
    """
    # Verificamos que el nombre de usuario no esté tomado
    usuario_existente = db.query(Usuario).filter(Usuario.nombre == datos.nombre).first()
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail=f"El usuario '{datos.nombre}' ya existe. Elegí otro nombre."
        )

    # Creamos el usuario con la contraseña encriptada
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        contrasena=encriptar_contrasena(datos.contrasena)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.post("/login", response_model=TokenRespuesta)
def iniciar_sesion(datos: LoginDatos, db: Session = Depends(get_db)):
    """
    Verifica usuario y contraseña.
    Si son correctos, devuelve un token JWT para usar en los demás endpoints.
    """
    # Buscamos el usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.nombre == datos.nombre).first()

    # Verificamos que exista y que la contraseña sea correcta
    if not usuario or not verificar_contrasena(datos.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos."
        )

    # Creamos el token con el nombre del usuario adentro
    token = crear_token({"sub": usuario.nombre})

    return {"access_token": token, "token_type": "bearer"}
