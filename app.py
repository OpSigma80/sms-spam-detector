import streamlit as st
import pickle
from procesamiento import SMSParser

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
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('svm_model.pkl', 'rb') as f:
        model = pickle.load(f)
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
    if mensaje:
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
    st.metric("Accuracy", "98.21%")
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