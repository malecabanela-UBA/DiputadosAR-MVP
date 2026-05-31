import pandas as pd

# =========================
# CARGA
# =========================

df = pd.read_csv(
    "raw_data/votos_macrocoaliciones.csv",
    encoding="utf-8-sig",
    low_memory=False
)

# =========================
# DIMENSION GENERAL
# =========================

print("\n==============================")
print("DIMENSION GENERAL")
print("==============================\n")

print("Filas:", len(df))
print("Columnas:", len(df.columns))

print("\nColumnas:")
print(df.columns.tolist())

# =========================
# MACROCOALICIONES
# =========================

print("\n==============================")
print("DISTRIBUCION MACROCOALICIONES")
print("==============================\n")

print(
    df["macrocoalicion"]
    .value_counts()
)

# =========================
# DISTRIBUCION VOTOS
# =========================

print("\n==============================")
print("DISTRIBUCION VOTOS")
print("==============================\n")

print(
    df["voto"]
    .value_counts()
)

# =========================
# VOTOS POR MACROCOALICION
# =========================

print("\n==============================")
print("VOTOS POR MACROCOALICION")
print("==============================\n")

tabla = pd.crosstab(
    df["macrocoalicion"],
    df["voto"],
    normalize="index"
) * 100

print(
    tabla.round(2)
)

# =========================
# AUSENTISMO
# =========================

print("\n==============================")
print("AUSENTISMO POR MACRO")
print("==============================\n")

aus = (
    df[df["voto"] == "AUSENTE"]
    .groupby("macrocoalicion")
    .size()
)

tot = (
    df.groupby("macrocoalicion")
    .size()
)

ausentismo = (
    (aus / tot) * 100
).sort_values(ascending=False)

print(
    ausentismo.round(2)
)

# =========================
# BLOQUES POR MACRO
# =========================

print("\n==============================")
print("CANTIDAD DE BLOQUES")
print("==============================\n")

bloques = (
    df.groupby("macrocoalicion")["bloque"]
    .nunique()
    .sort_values(ascending=False)
)

print(bloques)

# =========================
# TOP DIPUTADOS AUSENTISTAS
# =========================

print("\n==============================")
print("TOP AUSENTISTAS")
print("==============================\n")

top_aus = (
    df[df["voto"] == "AUSENTE"]
    ["diputado"]
    .value_counts()
    .head(20)
)

print(top_aus)

# =========================
# CONTROL OTROS
# =========================

print("\n==============================")
print("TOP OTROS")
print("==============================\n")

otros = (
    df[df["macrocoalicion"] == "OTROS"]
    ["bloque"]
    .value_counts()
    .head(50)
)

print(otros)