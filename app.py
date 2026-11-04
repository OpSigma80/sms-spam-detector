import pickle
from pathlib import Path

import streamlit as st

from preprocessing import SMSParser

# Configuración de la página
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="centered"
)

# Título
st.title("📱 Detector de Spam en SMS")
st.markdown("### Clasifica mensajes SMS como HAM o SPAM usando Machine Learning")

# Cargar modelo
@st.cache_resource
def load_model():
    project_dir = Path(__file__).resolve().parent
    vectorizer_path = project_dir / "tfidf_vectorizer.pkl"
    model_path = project_dir / "svm_model.pkl"

    if not vectorizer_path.exists() or not model_path.exists():
        return None, None

    with vectorizer_path.open("rb") as file:
        vectorizer = pickle.load(file)
    with model_path.open("rb") as file:
        model = pickle.load(file)
    return vectorizer, model

vectorizer, model = load_model()
parser = SMSParser()

# Input del usuario
mensaje = st.text_area(
    "Escribe o pega un mensaje SMS:",
    height=150,
    placeholder="Ejemplo: Congratulations! You won a free iPhone..."
)

# Botón de predicción
if st.button("🔍 Analizar Mensaje", type="primary"):
    if vectorizer is None or model is None:
        st.error("Modelo no disponible. Ejecuta `python procesamiento.py` para entrenarlo primero.")
    elif mensaje:
        # Procesar
        with st.spinner("Analizando..."):
            msg_procesado = parser.parse(mensaje)
            msg_vectorizado = vectorizer.transform([msg_procesado]).toarray()
            prediccion = model.predict(msg_vectorizado)[0]
        
        # Mostrar resultado
        if prediccion == "spam":
            st.error("🚨 **¡SPAM DETECTADO!**")
            st.warning("Este mensaje parece ser spam o phishing.")
        else:
            st.success("✅ **Mensaje Legítimo (HAM)**")
            st.info("Este mensaje parece ser seguro.")
        
        # Detalles técnicos
        with st.expander("📊 Ver detalles del procesamiento"):
            st.write(f"**Mensaje original:** {mensaje}")
            st.write(f"**Procesado:** {msg_procesado}")
            st.write(f"**Predicción:** {prediccion.upper()}")
    else:
        st.warning("⚠️ Por favor escribe un mensaje primero.")

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Información del Modelo")
    st.metric("Accuracy", "No publicada")
    st.metric("Modelo", "SVM + TF-IDF")
    st.metric("Dataset", "5,574 SMS")
    
    st.markdown("---")
    st.markdown("### 📚 Acerca de")
    st.markdown("""
    Este clasificador usa:
    - **SVM** (Support Vector Machine)
    - **TF-IDF** Vectorization
    - **NLP** para procesar texto
    """)
    
    st.markdown("---")
    st.markdown("**Creado por:** Tu Nombre")
    st.markdown("[GitHub](https://github.com/tu-usuario) | [LinkedIn](https://linkedin.com/in/tu-perfil)")

# Footer
st.markdown("---")
st.caption("⚠️ Nota: El modelo está entrenado con SMS en inglés. Los resultados pueden variar con mensajes en otros idiomas.")