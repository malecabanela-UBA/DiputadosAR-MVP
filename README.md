# 🏛️ Predictor de Votaciones Legislativas - Cámara de Diputados AR

**Seminario de Ciencia de Datos para Politólogos — UBA**

Aplicación web que permite visualizar y predecir el comportamiento de voto de los diputados argentinos usando Machine Learning.

---

## 🎯 ¿Qué hace?

- **Login seguro** con usuario y contraseña encriptada
- **Dashboard interactivo** con gráficos de votaciones por bloque y provincia
- **Predicción de voto** usando un modelo Random Forest entrenado con datos reales de la Cámara de Diputados
- **API REST** construida con FastAPI

---

## 🗂️ Estructura del proyecto

```
DiputadosAR/
├── BACKEND/
│   ├── main.py              → punto de entrada de la API
│   ├── database.py          → conexión a la BD y definición de tablas
│   ├── schemas.py           → validación de datos con Pydantic
│   ├── auth.py              → encriptación y tokens JWT
│   ├── rutas_auth.py        → endpoints de login y registro
│   └── rutas_votaciones.py  → endpoints de votaciones y predicción
├── FRONTEND/
│   └── app.py               → interfaz web con Streamlit
├── MODELO/
│   ├── entrenar_modelo.py   → script de entrenamiento
│   └── modelo_votacion.pkl  → modelo entrenado (generado al correr el script)
├── DATOS/
│   └── votaciones_limpio.csv
├── ANALISIS/
│   └── exploracion.ipynb
├── requirements.txt
└── .gitignore
```

---

## 🚀 Cómo instalar y correr

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/DiputadosAR.git
cd DiputadosAR
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Entrenar el modelo
```bash
cd MODELO
python entrenar_modelo.py
```

### 4. Correr el backend (en una terminal)
```bash
cd BACKEND
uvicorn main:app --reload
```

### 5. Correr el frontend (en otra terminal)
```bash
cd FRONTEND
streamlit run app.py
```

### 6. Abrir en el navegador
- **Frontend:** http://localhost:8501
- **Documentación de la API:** http://localhost:8000/docs

---

## 🔑 Credenciales de prueba

Crear una cuenta desde la pantalla de login, o usar:
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 🌐 Deploy

- **Backend:** [https://diputadosar.onrender.com](https://diputadosar.onrender.com) *(próximamente)*
- **Frontend:** [https://diputadosar.streamlit.app](https://diputadosar.streamlit.app) *(próximamente)*

---

## 🛠️ Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI + SQLAlchemy |
| Base de datos | SQLite (local) / PostgreSQL con Supabase (producción) |
| Autenticación | JWT + bcrypt |
| Machine Learning | Scikit-Learn (Random Forest) |
| Frontend | Streamlit + Plotly |
| Deploy | Render + Streamlit Community Cloud |
