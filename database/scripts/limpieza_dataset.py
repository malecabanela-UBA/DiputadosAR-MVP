import pandas as pd

# =========================
# CARGA
# =========================

df = pd.read_csv(
    "raw_data/votos_expandidos.csv",
    encoding="utf-8-sig"
)

print("\nFILAS INICIALES:", len(df))

# =========================
# LIMPIEZA VOTOS
# =========================

df = df[
    ~df["voto"].isin([
        "PRESIDENTE",
        "SIN_DATO"
    ])
]

# =========================
# LIMPIEZA PROVINCIAS
# =========================

df["provincia"] = df["provincia"].replace({
    "Capital Federal": "C.A.B.A."
})

df = df[
    ~df["provincia"].isin([
        "-",
        "SIN_DATO"
    ])
]

# =========================
# FECHAS
# =========================

df["fecha_dt"] = pd.to_datetime(
    df["fecha"],
    format="%d/%m/%Y - %H:%M",
    errors="coerce"
)

df["anio"] = df["fecha_dt"].dt.year

# =========================
# CONTROL
# =========================

print("\nFILAS FINALES:", len(df))

print("\nDISTRIBUCION DE VOTOS:")
print(df["voto"].value_counts())

print("\nPROVINCIAS:")
print(df["provincia"].value_counts())

print("\nRANGO TEMPORAL:")
print(df["anio"].min(), "-", df["anio"].max())

# =========================
# EXPORT
# =========================

df.to_csv(
    "raw_data/votos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivo generado:")
print("raw_data/votos_limpios.csv")