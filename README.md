🏛️ DiputadosAR - Modelo Predictivo de Votación Legislativa

👥 Información General

Integrantes: Gianfranco Crichigno, Malena Cabanela, Alma Daubenfeld

Proyecto: DiputadosAR


🎯 Planteo del Proyecto

El objetivo del proyecto es desarrollar una herramienta predictiva que permita anticipar el comportamiento de voto de los diputados de la Nación Argentina. A través de un modelo de Machine Learning entrenado con datos históricos reales, el sistema identifica patrones en la disciplina partidaria, la trayectoria legislativa y los alineamientos políticos para predecir si un diputado votará Afirmativo, Negativo o se Abstendrá ante un proyecto de ley.


⚠️ Planteo del Problema

Anticipar las intenciones de voto legislativo es difícil cuando la información disponible es ambivalente o proviene de fuentes de opinión pública poco estructuradas. Sin embargo, existen patrones observables y medibles: el bloque partidario al que pertenece un legislador, su comportamiento histórico de voto, las dinámicas de alineamiento entre bloques y la trayectoria individual del diputado. Este proyecto busca capturar y modelar esos patrones para hacer el comportamiento legislativo más transparente y anticipable.


📋 Requerimientos del Proyecto

RequerimientoDescripciónNombre del ProyectoDiputadosAR - Modelo Predictivo de Votación LegislativaEl ProblemaDificultad de anticipar intenciones de voto a partir de patrones observables: bloque partidario, comportamiento histórico, alineamientos y trayectoria del legisladorEl UsuarioInvestigadores y académicos, estudiantes de Ciencia Política, periodistas, consultoras políticas y público general interesadoOrigen de los DatosDatabase de "Cómo Votó" y webscraping del sitio oficial de la Honorable Cámara de Diputados de la NaciónFuncionalidadPredicción del voto de un diputado (Afirmativo / Negativo / Abstención) según su bloque, provincia y tipo de proyecto


🗂️ Estructura del Proyecto

DiputadosAR/
├── BACKEND/
│   ├── main.py              → punto de entrada de la API
│   ├── database.py          → conexión a la base de datos y tablas
│   ├── schemas.py           → validación de datos con Pydantic
│   ├── auth.py              → encriptación y tokens JWT
│   ├── rutas_auth.py        → endpoints de login y registro
│   └── rutas_votaciones.py  → endpoints de votaciones y predicción
├── FRONTEND/
│   └── app.py               → interfaz web con Streamlit
├── MODELO/
│   ├── entrenar_modelo.py   → script de entrenamiento del modelo
│   └── modelo_votacion.pkl  → modelo entrenado (Random Forest)
├── DATOS/
│   └── votaciones_limpio.csv
├── ANALISIS/
│   └── exploracion.ipynb
├── requirements.txt
└── .gitignore


🛠️ Stack Tecnológico

CapaHerramientasLenguajePythonManipulación de datospandas, numpyMachine Learningscikit-learn (Random Forest)VisualizaciónPlotly, seaborn, matplotlibBackend / APIFastAPI, uvicornFrontendStreamlitAutenticaciónJWT + bcryptBase de datosSQLite (local) / PostgreSQL con Supabase (producción)DeployRender + Streamlit Community CloudControl de versionesGit + GitHub


🔑 Credenciales de Prueba


Usuario: admin
Contraseña: admin123