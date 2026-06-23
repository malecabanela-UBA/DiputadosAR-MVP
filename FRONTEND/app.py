# app.py
# Este es el frontend de nuestra aplicación, hecho con Streamlit.
# Tiene varias páginas: Login, Dashboard, Predicciones
#
# Para correrlo: streamlit run app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------
st.set_page_config(
    page_title="Votaciones Legislativas 🇦🇷",
    page_icon="🏛️",
    layout="wide"
)

# URL de nuestra API (en local es esta, en producción la reemplazamos con la de Render)
API_URL = "http://127.0.0.1:8000"


# -----------------------------------------------------------
# SESSION STATE
# st.session_state guarda información entre clics
# Lo usamos para mantener al usuario logueado
# -----------------------------------------------------------
if "token" not in st.session_state:
    st.session_state.token = None          # el token JWT del usuario
if "usuario" not in st.session_state:
    st.session_state.usuario = None        # el nombre del usuario logueado


# -----------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------
def hacer_pedido(metodo: str, endpoint: str, datos: dict = None) -> dict:
    """
    Función que hace pedidos a la API.
    Agrega el token automáticamente si el usuario está logueado.
    """
    url = f"{API_URL}{endpoint}"
    headers = {}

    # Si tenemos token, lo agregamos al encabezado
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    try:
        if metodo == "GET":
            respuesta = requests.get(url, headers=headers)
        elif metodo == "POST":
            respuesta = requests.post(url, json=datos, headers=headers)

        return respuesta.json()
    except Exception as e:
        return {"error": f"No se pudo conectar con la API: {e}"}


# -----------------------------------------------------------
# PÁGINAS
# -----------------------------------------------------------

def pagina_login():
    """Página de inicio de sesión y registro"""
    st.title("🏛️ Sistema de Votaciones Legislativas")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Iniciar Sesión")
        with st.form("form_login"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            boton_login = st.form_submit_button("Entrar")

        if boton_login:
            respuesta = hacer_pedido("POST", "/auth/login", {
                "nombre": usuario,
                "contrasena": contrasena
            })
            if "access_token" in respuesta:
                # Guardamos el token en session_state para no pedirlo de nuevo
                st.session_state.token = respuesta["access_token"]
                st.session_state.usuario = usuario
                st.success(f"¡Bienvenido, {usuario}! 👋")
                st.rerun()  # recargamos para ir al dashboard
            else:
                st.error("Usuario o contraseña incorrectos.")

    with col2:
        st.subheader("Registrarse")
        with st.form("form_registro"):
            nuevo_usuario = st.text_input("Nuevo usuario")
            nueva_contrasena = st.text_input("Nueva contraseña", type="password")
            boton_registro = st.form_submit_button("Crear cuenta")

        if boton_registro:
            respuesta = hacer_pedido("POST", "/auth/registrar", {
                "nombre": nuevo_usuario,
                "contrasena": nueva_contrasena
            })
            if "id" in respuesta:
                st.success("¡Cuenta creada! Ahora podés iniciar sesión.")
            else:
                st.error(respuesta.get("detail", "Error al crear la cuenta."))


def pagina_dashboard():
    """Página principal con visualizaciones de votaciones"""
    st.title("📊 Dashboard de Votaciones")
    st.markdown(f"Bienvenido, **{st.session_state.usuario}** | [Cerrar sesión](#)")

    # Obtenemos los datos de la API
    votaciones = hacer_pedido("GET", "/votaciones/")

    if "error" in votaciones:
        st.error(votaciones["error"])
        return

    if not votaciones:
        st.info("Todavía no hay votaciones cargadas.")
        return

    # Convertimos a DataFrame para graficar
    df = pd.DataFrame(votaciones)

    # Métricas rápidas en la parte superior
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de votaciones", len(df))
    with col2:
        st.metric("Diputados únicos", df["diputado"].nunique())
    with col3:
        st.metric("Bloques", df["bloque"].nunique())

    st.markdown("---")

    # Gráfico 1: distribución de votos
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("¿Cómo votaron?")
        conteo_votos = df["voto"].value_counts().reset_index()
        conteo_votos.columns = ["Voto", "Cantidad"]
        fig1 = px.pie(
            conteo_votos,
            values="Cantidad",
            names="Voto",
            color_discrete_map={
                "AFIRMATIVO": "#2ecc71",
                "NEGATIVO": "#e74c3c",
                "ABSTENCION": "#95a5a6"
            }
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_der:
        st.subheader("Votos por bloque")
        votos_bloque = df.groupby(["bloque", "voto"]).size().reset_index(name="cantidad")
        fig2 = px.bar(
            votos_bloque,
            x="bloque",
            y="cantidad",
            color="voto",
            barmode="group",
            color_discrete_map={
                "AFIRMATIVO": "#2ecc71",
                "NEGATIVO": "#e74c3c",
                "ABSTENCION": "#95a5a6"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabla completa
    st.subheader("Todas las votaciones")
    st.dataframe(df, use_container_width=True)


def pagina_cargar_votacion():
    """Página para ingresar una votación nueva"""
    st.title("➕ Registrar Votación")

    with st.form("form_votacion"):
        col1, col2 = st.columns(2)

        with col1:
            diputado = st.text_input("Nombre del diputado/a")
            bloque = st.selectbox("Bloque", ["UCR", "PJ", "PRO", "Otro"])
            provincia = st.selectbox("Provincia", [
                "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza",
                "Tucumán", "Entre Ríos", "Salta", "Misiones", "Otra"
            ])

        with col2:
            tipo_proyecto = st.selectbox("Tipo de proyecto", [
                "ley", "resolución", "decreto", "declaración"
            ])
            voto = st.selectbox("Voto", ["AFIRMATIVO", "NEGATIVO", "ABSTENCION"])

        enviado = st.form_submit_button("Guardar votación")

    if enviado:
        respuesta = hacer_pedido("POST", "/votaciones/", {
            "diputado": diputado,
            "bloque": bloque,
            "provincia": provincia,
            "tipo_proyecto": tipo_proyecto,
            "voto": voto
        })
        if "id" in respuesta:
            st.success(f"✅ Votación de {diputado} guardada correctamente.")
        else:
            st.error("Error al guardar la votación.")


def pagina_predicciones():
    """Página para hacer predicciones con el modelo de ML"""
    st.title("🤖 Predicción de Voto")
    st.markdown("Completá los datos y el modelo predice cómo va a votar el diputado.")

    with st.form("form_prediccion"):
        col1, col2, col3 = st.columns(3)

        with col1:
            bloque = st.selectbox("Bloque político", ["UCR", "PJ", "PRO", "Otro"])
        with col2:
            provincia = st.selectbox("Provincia", [
                "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza",
                "Tucumán", "Entre Ríos", "Salta", "Misiones", "Otra"
            ])
        with col3:
            tipo_proyecto = st.selectbox("Tipo de proyecto", [
                "ley", "resolución", "decreto", "declaración"
            ])

        predecir = st.form_submit_button("¿Cómo va a votar?")

    if predecir:
        respuesta = hacer_pedido("POST", "/votaciones/predecir", {
            "bloque": bloque,
            "provincia": provincia,
            "tipo_proyecto": tipo_proyecto
        })

        if "voto_predicho" in respuesta:
            voto = respuesta["voto_predicho"]
            confianza = respuesta["confianza"] * 100

            # Mostramos el resultado con color según el voto
            colores = {
                "AFIRMATIVO": "🟢",
                "NEGATIVO": "🔴",
                "ABSTENCION": "⚪"
            }
            emoji = colores.get(voto, "❓")

            st.markdown("---")
            st.subheader("Resultado de la predicción")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(f"{emoji} Voto predicho", voto)
            with col_b:
                st.metric("Confianza del modelo", f"{confianza:.0f}%")
        else:
            st.error("No se pudo obtener la predicción. Verificá que la API esté corriendo.")


# -----------------------------------------------------------
# NAVEGACIÓN PRINCIPAL
# -----------------------------------------------------------
def main():
    # Si el usuario no está logueado, mostramos el login
    if not st.session_state.token:
        pagina_login()
        return

    # Si está logueado, mostramos el menú lateral
    with st.sidebar:
        st.title("🏛️ Menú")
        st.markdown(f"👤 **{st.session_state.usuario}**")
        st.markdown("---")

        pagina = st.radio("Ir a:", [
            "📊 Dashboard",
            "➕ Cargar votación",
            "🤖 Predicciones"
        ])

        st.markdown("---")
        if st.button("Cerrar sesión"):
            st.session_state.token = None
            st.session_state.usuario = None
            st.rerun()

    # Mostramos la página seleccionada
    if pagina == "📊 Dashboard":
        pagina_dashboard()
    elif pagina == "➕ Cargar votación":
        pagina_cargar_votacion()
    elif pagina == "🤖 Predicciones":
        pagina_predicciones()


if __name__ == "__main__":
    main()
