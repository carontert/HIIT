import streamlit as st
import gspread
import google.generativeai as genai
from google.oauth2.service_account import Credentials

# --- Configuración y Título de la App ---
st.set_page_config(page_title="Analista de Ejercicio", page_icon="🏋️")
st.title("🏋️ Tu Analista de Ejercicio Personal")
st.write("Presiona el botón para analizar los datos de tu Google Sheet 'ejercicio'.")

# --- Función para conectar y analizar ---
def analizar_entrenamiento():
    try:
        # Conexión a Google Sheets usando los "Secrets" de Streamlit
        creds_dict = st.secrets["gcp_service_account"]
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)

        # Conexión a Gemini API
        genai.configure(api_key=st.secrets["gemini_api_key"])

        # Leer datos del Google Sheet
        spreadsheet = gc.open("HIIT")
        worksheet = spreadsheet.sheet1
        datos_entrenamiento = worksheet.get_all_records()

        if not datos_entrenamiento:
            st.warning("El archivo 'ejercicio' está vacío o no se pudo leer.")
            return

        # Crear el prompt para Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analiza los siguientes datos de mis sesiones de entrenamiento.
        Datos: {datos_entrenamiento}

        Basado en estos datos, calcula y presenta un resumen amigable con:
        1. El total de calorías quemadas.
        2. El tiempo total de entrenamiento.
        3. Un pequeño resumen motivacional.

        Usa formato Markdown con títulos, negritas y emojis.
        """

        # Generar y mostrar respuesta
        response = model.generate_content(prompt)
        st.markdown(response.text)

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Error: No se encontró el archivo 'ejercicio'. Asegúrate de que el nombre es correcto.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        st.info("Asegúrate de haber compartido tu Google Sheet con el correo electrónico del 'client_email' que está en tus Secrets.")

# --- Creación del Botón ---
if st.button("💪 Analizar mi Entrenamiento"):
    with st.spinner("Conectando con tus datos y analizando..."):
        analizar_entrenamiento()
