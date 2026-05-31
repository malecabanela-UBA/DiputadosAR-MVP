import pandas as pd

df = pd.read_csv(
    "raw_data/votos_macrocoaliciones.csv",
    encoding="utf-8-sig",
    low_memory=False
)

df["fecha_dt"] = pd.to_datetime(
    df["fecha"],
    format="%d/%m/%Y - %H:%M",
    errors="coerce"
)

df = df.dropna(subset=["fecha_dt"])
df = df.sort_values(["fecha_dt", "votacion_id"]).reset_index(drop=True)

df["anio"] = df["fecha_dt"].dt.year
df["mes"] = df["fecha_dt"].dt.month

df["target_afirmativo"] = (df["voto"] == "AFIRMATIVO").astype(int)

df["es_ausente"] = (df["voto"] == "AUSENTE").astype(int)
df["es_negativo"] = (df["voto"] == "NEGATIVO").astype(int)
df["es_abstencion"] = (df["voto"] == "ABSTENCION").astype(int)

df["tasa_afirmativos_previos"] = (
    df.groupby("diputado")["target_afirmativo"]
    .transform(lambda x: x.shift(1).expanding().mean() * 100)
)

df["tasa_ausencias_previas"] = (
    df.groupby("diputado")["es_ausente"]
    .transform(lambda x: x.shift(1).expanding().mean() * 100)
)

df["tasa_negativos_previos"] = (
    df.groupby("diputado")["es_negativo"]
    .transform(lambda x: x.shift(1).expanding().mean() * 100)
)

df["tasa_abstenciones_previas"] = (
    df.groupby("diputado")["es_abstencion"]
    .transform(lambda x: x.shift(1).expanding().mean() * 100)
)

df["total_votos_previos"] = (
    df.groupby("diputado")["voto"]
    .transform(lambda x: x.shift(1).expanding().count())
)

cols_hist = [
    "tasa_afirmativos_previos",
    "tasa_ausencias_previas",
    "tasa_negativos_previos",
    "tasa_abstenciones_previas",
    "total_votos_previos"
]

df[cols_hist] = df[cols_hist].fillna(0)

# Split cronológico por votación
votaciones = (
    df[["votacion_id", "fecha_dt"]]
    .drop_duplicates()
    .sort_values("fecha_dt")
)

n = len(votaciones)

train_end = int(n * 0.70)
val_end = int(n * 0.85)

train_ids = votaciones.iloc[:train_end]["votacion_id"]
val_ids = votaciones.iloc[train_end:val_end]["votacion_id"]
test_ids = votaciones.iloc[val_end:]["votacion_id"]

df["split"] = "none"
df.loc[df["votacion_id"].isin(train_ids), "split"] = "train"
df.loc[df["votacion_id"].isin(val_ids), "split"] = "validation"
df.loc[df["votacion_id"].isin(test_ids), "split"] = "test"

df.to_csv(
    "raw_data/dataset_features_base.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Dataset generado:")
print(df["split"].value_counts())
print("\nDistribución target por split:")
print(pd.crosstab(df["split"], df["target_afirmativo"], normalize="index").round(3) * 100)