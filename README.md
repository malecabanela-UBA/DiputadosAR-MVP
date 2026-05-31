# DiputadosAR 🏛️

### Modelo Predictivo de Votación Legislativa — Cámara de Diputados de la Nación Argentina

> Proyecto Final — Ciencia de Datos para Politólogos
> Carrera de Ciencia Política — Universidad de Buenos Aires
> Integrantes: Gianfranco Crichigno · Malena Cabanela · Alma Daubenfeld

---

# ¿Qué es DiputadosAR?

DiputadosAR es un modelo de Machine Learning diseñado para predecir el comportamiento de voto de los diputados nacionales argentinos a partir de patrones históricos observables.

El objetivo del proyecto no es analizar el contenido de los proyectos de ley sino modelar el comportamiento legislativo individual utilizando información acumulada de votaciones previas.

La pregunta central del trabajo es:

> Dado un diputado, su bloque partidario, su provincia y su historial de votación, ¿es posible anticipar cómo votará en una futura sesión parlamentaria?

---

# Fuentes de datos

| Fuente           | Descripción                                                         |
| ---------------- | ------------------------------------------------------------------- |
| Cómo Votó        | Base histórica de votaciones nominales de la Cámara de Diputados    |
| Diputados.gov.ar | Información complementaria para validación y análisis institucional |

---

# Dataset

## Dimensión general

| Métrica            | Valor       |
| ------------------ | ----------- |
| Observaciones      | 743.970     |
| Votaciones         | 2.913       |
| Diputados únicos   | 2.071       |
| Bloques originales | 304         |
| Provincias         | 27          |
| Rango temporal     | 1993 – 2026 |

# Dataset

## Dimensión general

| Métrica            | Valor       |
| ------------------ | ----------- |
| Observaciones      | 743.970     |
| Votaciones         | 2.913       |
| Diputados únicos   | 2.071       |
| Bloques originales | 304         |
| Provincias         | 27          |
| Rango temporal     | 1993 – 2026 |

## Distribución del voto

| Voto       | Casos   |
| ---------- | ------- |
| AFIRMATIVO | 419.500 |
| AUSENTE    | 175.266 |
| NEGATIVO   | 132.745 |
| ABSTENCIÓN | 16.459  |

Las ausencias fueron conservadas como comportamiento legislativo válido y no fueron tratadas como datos faltantes.

Se consideró que la ausencia constituye una estrategia legislativa observable y, por lo tanto, representa información políticamente relevante para el modelo.

---

# Construcción de macrocoaliciones

Los 304 bloques legislativos fueron agrupados manualmente en siete macrocoaliciones para capturar afinidades parlamentarias de largo plazo.

## Macrocoaliciones utilizadas

* PERONISMO
* RADICALISMO
* PRO
* LLA
* IZQUIERDA
* PROVINCIALES
* OTROS

La clasificación fue realizada utilizando evidencia política, alianzas parlamentarias y comportamiento legislativo histórico.

---

# Pipeline del proyecto

```text
JSON originales
        │
        ▼
Expansión de votos nominales
        │
        ▼
Limpieza y normalización
        │
        ▼
Clasificación de bloques
en macrocoaliciones
        │
        ▼
Feature Engineering
(sin data leakage)
        │
        ▼
Train / Validation / Test
(split temporal)
        │
        ▼
Random Forest
        │
        ▼
Evaluación y exportación
de métricas y modelos
```

---

# Feature Engineering

El modelo utiliza exclusivamente variables derivadas del comportamiento histórico de los legisladores.

## Variables utilizadas

### Variables políticas

* Macrocoalición
* Provincia

### Variables históricas

* Tasa histórica de votos afirmativos
* Tasa histórica de votos negativos
* Tasa histórica de abstenciones
* Tasa histórica de ausencias
* Total de votos previos

### Variables temporales

* Año
* Mes

---

# Prevención de Data Leakage

Uno de los principales desafíos metodológicos del proyecto fue evitar data leakage.

Las variables históricas fueron construidas utilizando un esquema de expanding window:

* cada observación utiliza únicamente información disponible hasta ese momento;
* nunca se utilizan votos futuros;
* el voto que se intenta predecir no participa en el cálculo de sus propias variables históricas.

De esta forma, el modelo reproduce condiciones realistas de predicción.

---

# Separación de conjuntos

La división del dataset se realizó de manera cronológica para preservar la estructura temporal de las votaciones y evitar contaminación entre conjuntos.

| Conjunto   | Observaciones |
| ---------- | ------------: |
| Train      |       520.991 |
| Validation |       111.169 |
| Test       |       111.810 |


| Conjunto   |    Proporción |
| ---------- | ------------: |
| Train      |           70% |
| Validation |           15% |
| Test       |           15% |

No se utilizó separación aleatoria debido al riesgo de data leakage temporal y a la necesidad de reproducir condiciones realistas de predicción.

No se utilizó separación aleatoria debido al riesgo de data leakage temporal y a la necesidad de reproducir condiciones realistas de predicción.


---

# Modelo

## Algoritmo

Random Forest Classifier

## Configuración

* 100 árboles
* Class Weight = Balanced
* Profundidad máxima = 12

---

# Resultados

## Validation Set

* Accuracy: 60.9%
* F1 Score: 0.714

## Test Set

* Accuracy: 52.5%
* F1 Score: 0.635

La diferencia entre Validation y Test sugiere la existencia de cambios estructurales en el sistema político argentino a lo largo del período analizado.

---

# Estructura del repositorio

```text
DiputadosAR/

├── database/
│   └── scripts/
│       ├── generar_votos_expandidos.py
│       ├── limpieza_dataset.py
│       └── construir_macrocoaliciones.py
│
├── analysis/
│   ├── eda_basico.py
│   └── eda_macrocoaliciones.py
│
├── modeling/
│   ├── feature_engineering.py
│   └── modelo_random_forest.py
│
├── raw_data/
│
├── outputs/
│   ├── figures/
│   ├── metrics/
│   └── models/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Cómo ejecutar el proyecto

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Construcción del dataset

```bash
python database/scripts/generar_votos_expandidos.py
python database/scripts/limpieza_dataset.py
python database/scripts/construir_macrocoaliciones.py
```

## Generación de features

```bash
python modeling/feature_engineering.py
```

Genera:

```text
raw_data/dataset_features_base.csv
```

El archivo `dataset_features_base.csv` no se incluye en el repositorio debido a su tamaño (aproximadamente 324 MB). Puede regenerarse localmente ejecutando el proceso de Feature Engineering.

## Entrenamiento y evaluación

```bash
python modeling/modelo_random_forest.py
```

---

# Outputs generados

El pipeline genera automáticamente:

## Métricas

* metricas_random_forest.csv
* feature_importance.csv
* accuracy_por_macrocoalicion.csv

## Visualizaciones

* confusion_matrix_test.png
* feature_importance.png
* accuracy_por_macrocoalicion.png

## Modelo entrenado

* random_forest_pipeline.pkl

El modelo entrenado se exporta automáticamente para garantizar reproducibilidad, permitir inspección posterior y facilitar futuras etapas de análisis o despliegue.

---

# Limitaciones

El modelo fue diseñado para predecir comportamiento legislativo a partir de patrones históricos.

No incorpora:

* contenido textual de los proyectos de ley;
* contexto político coyuntural;
* negociaciones parlamentarias;
* eventos externos.

Por lo tanto, los errores del modelo pueden interpretarse como cambios políticos, rupturas de disciplina partidaria o comportamientos legislativos atípicos.

---

# Licencia

Proyecto desarrollado con fines académicos en el marco de la materia Ciencia de Datos para Politólogos de la Universidad de Buenos Aires.
