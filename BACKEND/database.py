# database.py
# Este archivo se encarga de conectarse a la base de datos
# y de crear las tablas si no existen todavía

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS
# Por ahora usamos SQLite (un archivo local, sin configurar nada)
# Cuando tengamos Supabase, solo hay que cambiar esta línea
# -----------------------------------------------------------
DATABASE_URL = "sqlite:///./diputados.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necesario solo para SQLite
)

# Esto es como una "plantilla" para nuestros modelos de tabla
Base = declarative_base()

# Session es lo que usamos para hacer consultas a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -----------------------------------------------------------
# TABLAS DE LA BASE DE DATOS
# Cada clase acá representa una tabla
# -----------------------------------------------------------

class Usuario(Base):
    """Tabla que guarda los usuarios del sistema"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)   # nombre de usuario (único)
    contrasena = Column(String)                         # contraseña encriptada


class Votacion(Base):
    """Tabla que guarda las votaciones de los diputados"""
    __tablename__ = "votaciones"

    id = Column(Integer, primary_key=True, index=True)
    diputado = Column(String, index=True)    # nombre del diputado
    bloque = Column(String)                  # bloque político al que pertenece
    provincia = Column(String)               # provincia que representa
    tipo_proyecto = Column(String)           # tipo de proyecto (ley, resolución, etc.)
    voto = Column(String)                    # cómo votó: AFIRMATIVO, NEGATIVO, ABSTENCION


# -----------------------------------------------------------
# FUNCIÓN AUXILIAR
# La usamos en cada endpoint para obtener una sesión de BD
# -----------------------------------------------------------
def get_db():
    """Abre una sesión de base de datos y la cierra al terminar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear todas las tablas en la base de datos al iniciar
def crear_tablas():
    Base.metadata.create_all(bind=engine)
