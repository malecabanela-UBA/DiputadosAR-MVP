import pandas as pd
import matplotlib.pyplot as plt
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ======================================
# CARPETAS
# ======================================

OUTPUTS = Path("outputs")
FIGURES = OUTPUTS / "figures"
METRICS = OUTPUTS / "metrics"
MODELS = OUTPUTS / "models"

for folder in [OUTPUTS, FIGURES, METRICS, MODELS]:
    folder.mkdir(parents=True, exist_ok=True)

# ======================================
# CARGA DATASET
# ======================================

df = pd.read_csv(
    "raw_data/dataset_features_base.csv",
    encoding="utf-8-sig",
    low_memory=False
)

# ======================================
# FEATURES Y TARGET
# ======================================

FEATURES_NUM = [
    "tasa_afirmativos_previos",
    "tasa_ausencias_previas",
    "tasa_negativos_previos",
    "tasa_abstenciones_previas",
    "total_votos_previos",
    "anio",
    "mes"
]

FEATURES_CAT = [
    "macrocoalicion",
    "provincia"
]

FEATURES = FEATURES_NUM + FEATURES_CAT
TARGET = "target_afirmativo"

df_model = df[FEATURES + [TARGET, "split"]].dropna()

train = df_model[df_model["split"] == "train"]
val = df_model[df_model["split"] == "validation"]
test = df_model[df_model["split"] == "test"]

X_train = train[FEATURES]
y_train = train[TARGET]

X_val = val[FEATURES]
y_val = val[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

print("\n==============================")
print("DISTRIBUCION DE SPLITS")
print("==============================")
print("Train:     ", len(X_train))
print("Validation:", len(X_val))
print("Test:      ", len(X_test))

# ======================================
# PIPELINE
# ======================================

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES_CAT),
        ("num", "passthrough", FEATURES_NUM)
    ]
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", model)
    ]
)

# ======================================
# ENTRENAMIENTO
# ======================================

print("\nEntrenando modelo...")
pipeline.fit(X_train, y_train)
print("Modelo entrenado.")

# ======================================
# VALIDATION
# ======================================

pred_val = pipeline.predict(X_val)

acc_val = accuracy_score(y_val, pred_val)
f1_val = f1_score(y_val, pred_val)

print("\n==============================")
print("VALIDATION")
print("==============================")
print("Accuracy:", round(acc_val, 4))
print("F1:", round(f1_val, 4))
print(confusion_matrix(y_val, pred_val))
print(classification_report(y_val, pred_val))

# ======================================
# TEST
# ======================================

pred_test = pipeline.predict(X_test)

acc_test = accuracy_score(y_test, pred_test)
f1_test = f1_score(y_test, pred_test)

print("\n==============================")
print("TEST")
print("==============================")
print("Accuracy:", round(acc_test, 4))
print("F1:", round(f1_test, 4))
print(confusion_matrix(y_test, pred_test))
print(classification_report(y_test, pred_test))

# ======================================
# EXPORT METRICAS
# ======================================

metricas = pd.DataFrame([
    {
        "split": "validation",
        "accuracy": acc_val,
        "f1_score": f1_val,
        "filas": len(X_val)
    },
    {
        "split": "test",
        "accuracy": acc_test,
        "f1_score": f1_test,
        "filas": len(X_test)
    }
])

metricas.to_csv(
    METRICS / "metricas_random_forest.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nMétricas exportadas:")
print(METRICS / "metricas_random_forest.csv")

# ======================================
# MATRIZ DE CONFUSION TEST
# ======================================

cm = confusion_matrix(y_test, pred_test)

fig, ax = plt.subplots(figsize=(7, 5))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["No Afirmativo", "Afirmativo"]
)

disp.plot(ax=ax, cmap="Blues", colorbar=False)

ax.set_title(
    "Matriz de Confusión — Test Set",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    FIGURES / "confusion_matrix_test.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("Matriz de confusión guardada:")
print(FIGURES / "confusion_matrix_test.png")

# ======================================
# FEATURE IMPORTANCE
# ======================================

feature_names = (
    pipeline.named_steps["preprocess"]
    .get_feature_names_out()
)

importancias = pd.DataFrame({
    "feature": feature_names,
    "importance": pipeline.named_steps["model"].feature_importances_
})

importancias = importancias.sort_values(
    "importance",
    ascending=False
)

importancias.to_csv(
    METRICS / "feature_importance.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Feature importance exportado:")
print(METRICS / "feature_importance.csv")

top_importancias = importancias.head(20).sort_values(
    "importance",
    ascending=True
)

fig, ax = plt.subplots(figsize=(9, 6))

ax.barh(
    top_importancias["feature"],
    top_importancias["importance"]
)

ax.set_xlabel("Importancia relativa")
ax.set_title(
    "Top 20 Feature Importance — Random Forest",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    FIGURES / "feature_importance.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("Gráfico feature importance guardado:")
print(FIGURES / "feature_importance.png")

# ======================================
# ACCURACY POR MACROCOALICION
# ======================================

df_test_eval = test.copy()
df_test_eval["y_real"] = y_test.values
df_test_eval["y_pred"] = pred_test
df_test_eval["correcto"] = (
    df_test_eval["y_real"] == df_test_eval["y_pred"]
).astype(int)

acc_macro = (
    df_test_eval
    .groupby("macrocoalicion")["correcto"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "accuracy", "count": "n_votos"})
    .sort_values("accuracy", ascending=True)
)

acc_macro.to_csv(
    METRICS / "accuracy_por_macrocoalicion.csv",
    encoding="utf-8-sig"
)

fig, ax = plt.subplots(figsize=(9, 6))

ax.barh(
    acc_macro.index,
    acc_macro["accuracy"] * 100
)

ax.axvline(
    x=acc_test * 100,
    linestyle="--",
    label="Accuracy global"
)

ax.set_xlabel("Accuracy (%)")
ax.set_title(
    "Accuracy por Macrocoalición — Test Set",
    fontsize=14,
    fontweight="bold"
)

ax.legend()

plt.tight_layout()

plt.savefig(
    FIGURES / "accuracy_por_macrocoalicion.png",
    dpi=150,
    bbox_inches="tight"
)

plt.close()

print("Accuracy por macrocoalición guardado:")
print(METRICS / "accuracy_por_macrocoalicion.csv")
print(FIGURES / "accuracy_por_macrocoalicion.png")

# ======================================
# EXPORT MODELO
# ======================================

joblib.dump(
    pipeline,
    MODELS / "random_forest_pipeline.pkl"
)

print("\nModelo exportado:")
print(MODELS / "random_forest_pipeline.pkl")

print("\n==============================")
print("SCRIPT COMPLETADO")
print("==============================")