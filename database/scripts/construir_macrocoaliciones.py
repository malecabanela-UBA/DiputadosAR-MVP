import pandas as pd
import unicodedata
import re

def normalizar_texto(x):
    x = str(x).lower().strip()
    x = unicodedata.normalize("NFKD", x)
    x = x.encode("ascii", "ignore").decode("ascii")
    x = re.sub(r"[^a-z0-9]+", " ", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x

df = pd.read_csv(
    "raw_data/votos_limpios.csv",
    encoding="utf-8-sig",
    low_memory=False
)

clasif = pd.read_csv(
    "raw_data/clasificacion_bloques.csv",
    encoding="utf-8-sig",
    low_memory=False
)

clasif["bloque_key"] = clasif["partido"].apply(normalizar_texto)
df["bloque_key"] = df["bloque"].apply(normalizar_texto)

mapa_bloques = dict(
    zip(
        clasif["bloque_key"],
        clasif["macrocoalicion"]
    )
)

df["macrocoalicion"] = df["bloque_key"].map(mapa_bloques)
df["macrocoalicion"] = df["macrocoalicion"].fillna("OTROS")

print("\n==============================")
print("DISTRIBUCION MACROCOALICIONES")
print("==============================\n")
print(df["macrocoalicion"].value_counts())

print("\n==============================")
print("BLOQUES NO MAPEADOS")
print("==============================\n")

no_mapeados = (
    df[df["macrocoalicion"] == "OTROS"]
    ["bloque"]
    .value_counts()
    .head(100)
)

print(no_mapeados)

df = df.drop(columns=["bloque_key"])

df.to_csv(
    "raw_data/votos_macrocoaliciones.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivo generado:")
print("raw_data/votos_macrocoaliciones.csv")