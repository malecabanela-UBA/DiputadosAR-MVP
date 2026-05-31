import json
import pandas as pd

VOTE_DECODE = {
    0: "SIN_DATO",
    1: "AFIRMATIVO",
    2: "NEGATIVO",
    3: "ABSTENCION",
    4: "AUSENTE",
    5: "PRESIDENTE",
}

with open("raw_data/diputados.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("raw_data/hcdn_slug_map.json", "r", encoding="utf-8") as f:
    slug_map = json.load(f)

filas = []

for votacion in data["votaciones"]:
    votacion_id = str(votacion["id"])
    slug = slug_map.get(votacion_id, votacion.get("sl", ""))

    for voto in votacion["v"]:
        diputado_id, bloque_id, provincia_id, voto_id = voto

        filas.append({
            "votacion_id": votacion_id,
            "titulo": votacion.get("t", ""),
            "slug": slug,
            "fecha": votacion.get("d", "").replace("\n", " ").strip(),
            "resultado_general": votacion.get("r", ""),
            "tipo_votacion": votacion.get("tp", ""),
            "periodo": votacion.get("p", ""),
            "total_afirmativos": votacion.get("a", 0),
            "total_negativos": votacion.get("n", 0),
            "total_abstenciones": votacion.get("b", 0),
            "total_ausentes": votacion.get("u", 0),
            "diputado": data["names"][diputado_id] if diputado_id < len(data["names"]) else "SIN_DATO",
            "bloque": data["blocs"][bloque_id] if bloque_id < len(data["blocs"]) else "SIN_DATO",
            "provincia": data["provinces"][provincia_id] if provincia_id < len(data["provinces"]) else "SIN_DATO",
            "voto": VOTE_DECODE.get(voto_id, "DESCONOCIDO"),
        })

df = pd.DataFrame(filas)

df.to_csv("raw_data/votos_expandidos.csv", index=False, encoding="utf-8-sig")

print("Archivo generado correctamente:")
print("raw_data/votos_expandidos.csv")
print("Filas:", len(df))
print("Columnas:", list(df.columns))
print(df.head(10))