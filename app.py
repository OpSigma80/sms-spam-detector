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
st.title("📱 SMS Spam Detector")
st.markdown("### Classify SMS messages as HAM or SPAM using Machine Learning")

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

# User input
message = st.text_area(
    "Type or paste an SMS message:",
    height=150,
    placeholder="Example: Congratulations! You won a free iPhone..."
)

# Prediction button
if st.button("🔍 Analyze Message", type="primary"):
    if vectorizer is None or model is None:
        st.error("Model unavailable. Run `python train_model.py` to train it first.")
    elif message:
        # Process
        with st.spinner("Analyzing..."):
            processed_message = parser.parse(message)
            message_vector = vectorizer.transform([processed_message]).toarray()
            prediction = model.predict(message_vector)[0]
        
        # Show result
        if prediction == "spam":
            st.error("🚨 **SPAM DETECTED!**")
            st.warning("This message appears to be spam or phishing.")
        else:
            st.success("✅ **Legitimate Message (HAM)**")
            st.info("This message appears to be safe.")
        
        # Technical details
        with st.expander("📊 View processing details"):
            st.write(f"**Original message:** {message}")
            st.write(f"**Processed:** {processed_message}")
            st.write(f"**Prediction:** {prediction.upper()}")
    else:
        st.warning("⚠️ Please enter a message first.")

# Information sidebar
with st.sidebar:
    st.header("ℹ️ Model Information")
    st.metric("Test Accuracy", "98.48%")
    st.metric("Model", "SVM + TF-IDF")
    st.metric("Dataset", "5,574 SMS")
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    This classifier uses:
    - **SVM** (Support Vector Machine)
    - **TF-IDF** Vectorization
    - **NLP** for text processing
    """)
    
    st.markdown("---")
    st.markdown("**Created by:** Israel Sanchez")
    st.markdown("[GitHub](https://github.com/OpSigma80)")

# Footer
st.markdown("---")
st.caption("⚠️ Note: The model is trained on English SMS messages. Results may vary for messages in other languages.")