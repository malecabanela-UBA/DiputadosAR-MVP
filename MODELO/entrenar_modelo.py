# entrenar_modelo.py
# Este script entrena el modelo de Machine Learning y lo guarda en un archivo .pkl
# Solo hay que correrlo UNA VEZ (o cada vez que tengamos datos nuevos)
#
# Para correrlo: python entrenar_modelo.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import classification_report
import joblib
import os

print("📊 Cargando datos...")

# -----------------------------------------------------------
# CARGAR DATOS
# Intentamos cargar el CSV real. Si no existe, usamos datos de ejemplo.
# -----------------------------------------------------------
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "..", "DATOS", "votaciones_limpio.csv")

if os.path.exists(RUTA_DATOS):
    df = pd.read_csv(RUTA_DATOS)
    print(f"✅ Datos cargados: {len(df)} votaciones")
else:
    print("⚠️  No se encontró el CSV. Usando datos de ejemplo para demostración...")
    # Datos de ejemplo para que el modelo pueda entrenarse sin datos reales
    df = pd.DataFrame({
        "bloque": ["UCR", "PJ", "PRO", "UCR", "PJ", "PRO", "UCR", "PJ", "PRO", "UCR",
                   "PJ", "PRO", "UCR", "PJ", "PRO", "UCR", "PJ", "PRO", "UCR", "PJ"],
        "provincia": ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Buenos Aires",
                      "Córdoba", "Santa Fe", "Mendoza", "Buenos Aires", "Córdoba",
                      "Santa Fe", "Mendoza", "Buenos Aires", "Córdoba", "Santa Fe",
                      "Mendoza", "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza"],
        "tipo_proyecto": ["ley", "resolución", "ley", "decreto", "ley",
                          "resolución", "decreto", "ley", "resolución", "decreto",
                          "ley", "resolución", "decreto", "ley", "resolución",
                          "decreto", "ley", "resolución", "decreto", "ley"],
        "voto": ["AFIRMATIVO", "NEGATIVO", "AFIRMATIVO", "ABSTENCION", "NEGATIVO",
                 "AFIRMATIVO", "NEGATIVO", "AFIRMATIVO", "ABSTENCION", "NEGATIVO",
                 "AFIRMATIVO", "NEGATIVO", "AFIRMATIVO", "ABSTENCION", "NEGATIVO",
                 "AFIRMATIVO", "NEGATIVO", "AFIRMATIVO", "ABSTENCION", "NEGATIVO"]
    })

# -----------------------------------------------------------
# PREPARAR LOS DATOS
# -----------------------------------------------------------
# Variables que usa el modelo para predecir (features)
X = df[["bloque", "provincia", "tipo_proyecto"]]

# Lo que queremos predecir (target)
y = df["voto"]

# Dividimos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"📚 Datos de entrenamiento: {len(X_train)} registros")
print(f"🧪 Datos de prueba: {len(X_test)} registros")

# -----------------------------------------------------------
# CREAR EL MODELO
# Usamos un Pipeline para que el preprocesamiento y el modelo
# viajen juntos dentro del .pkl (así no hay que preprocesar aparte al predecir)
# -----------------------------------------------------------

# Primero convertimos texto a números (los árboles necesitan números)
preprocesador = ColumnTransformer(transformers=[
    ("categoricas", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
     ["bloque", "provincia", "tipo_proyecto"])
])

# Random Forest: construye muchos árboles de decisión y vota entre ellos
modelo = Pipeline(steps=[
    ("preprocesador", preprocesador),
    ("clasificador", RandomForestClassifier(
        n_estimators=100,   # 100 árboles en el bosque
        random_state=42     # para que los resultados sean reproducibles
    ))
])

# -----------------------------------------------------------
# ENTRENAR
# -----------------------------------------------------------
print("\n🌳 Entrenando el modelo Random Forest...")
modelo.fit(X_train, y_train)

# -----------------------------------------------------------
# EVALUAR
# -----------------------------------------------------------
print("\n📈 Resultados en datos de prueba:")
y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=0))

# -----------------------------------------------------------
# GUARDAR EL MODELO
# -----------------------------------------------------------
ruta_guardado = os.path.join(os.path.dirname(__file__), "modelo_votacion.pkl")
joblib.dump(modelo, ruta_guardado)
print(f"\n💾 Modelo guardado en: {ruta_guardado}")
print("✅ ¡Listo! Ahora podés correr la API y usar el endpoint de predicción.")
