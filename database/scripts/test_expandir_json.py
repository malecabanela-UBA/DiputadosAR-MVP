import json

with open("raw_data/diputados.json", "r", encoding="utf-8") as f:
    data = json.load(f)

VOTE_DECODE = {
    1: "AFIRMATIVO",
    2: "NEGATIVO",
    3: "ABSTENCION",
    4: "AUSENTE",
    5: "PRESIDENTE",
    0: "SIN_DATO",
}

primera_votacion = data["votaciones"][0]

print("ID:", primera_votacion["id"])
print("Título:", primera_votacion["t"])
print("Fecha:", primera_votacion["d"])
print("Resultado:", primera_votacion["r"])
print("Tipo:", primera_votacion["tp"])
print("Cantidad de votos:", len(primera_votacion["v"]))

print("\nPrimeros 10 votos expandidos:")

for voto in primera_votacion["v"][:10]:
    diputado_id, bloque_id, provincia_id, voto_id = voto

    diputado = data["names"][diputado_id]
    bloque = data["blocs"][bloque_id]
    provincia = data["provinces"][provincia_id]
    voto_texto = VOTE_DECODE.get(voto_id, "DESCONOCIDO")

    print(diputado, "|", bloque, "|", provincia, "|", voto_texto)