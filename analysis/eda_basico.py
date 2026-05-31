import pandas as pd

# =========================
# CARGA DEL DATASET
# =========================

df = pd.read_csv(
    "raw_data/votos_expandidos.csv",
    encoding="utf-8-sig"
)

print("\n==============================")
print("DIMENSION GENERAL DEL DATASET")
print("==============================\n")

print("Cantidad de filas:", len(df))
print("Cantidad de columnas:", len(df.columns))

print("\nColumnas:")
print(df.columns.tolist())

# =========================
# ENTIDADES PRINCIPALES
# =========================

print("\n==============================")
print("ENTIDADES PRINCIPALES")
print("==============================\n")

print("Diputados únicos:", df["diputado"].nunique())
print("Bloques únicos:", df["bloque"].nunique())
print("Provincias únicas:", df["provincia"].nunique())
print("Votaciones únicas:", df["votacion_id"].nunique())

# =========================
# TARGET
# =========================

print("\n==============================")
print("DISTRIBUCION DEL TARGET")
print("==============================\n")

print(df["voto"].value_counts())

# =========================
# TOP BLOQUES
# =========================

print("\n==============================")
print("TOP 15 BLOQUES")
print("==============================\n")

print(df["bloque"].value_counts().head(15))

# =========================
# TOP DIPUTADOS
# =========================

print("\n==============================")
print("TOP 15 DIPUTADOS CON MAS VOTOS")
print("==============================\n")

print(df["diputado"].value_counts().head(15))

# =========================
# PROVINCIAS
# =========================

print("\n==============================")
print("DISTRIBUCION POR PROVINCIA")
print("==============================\n")

print(df["provincia"].value_counts())

# =========================
# SIN DATO
# =========================

print("\n==============================")
print("CONTROL DE SIN_DATO")
print("==============================\n")

for columna in ["diputado", "bloque", "provincia", "voto"]:
    cantidad = (df[columna] == "SIN_DATO").sum()
    print(f"{columna}: {cantidad}")

# =========================
# FECHAS
# =========================

print("\n==============================")
print("MUESTRA DE FECHAS")
print("==============================\n")

print(df["fecha"].head(10))