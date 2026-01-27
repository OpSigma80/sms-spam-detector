# 📱 SMS Spam Detection con Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Accuracy](https://img.shields.io/badge/Accuracy-98.21%25-brightgreen)](README.md)

Clasificador automático de mensajes SMS usando técnicas de NLP y Machine Learning para detectar spam con **98.21% de precisión**.

---

## 🎯 Objetivo

Implementar un sistema profesional de detección de spam en mensajes SMS utilizando procesamiento de lenguaje natural (NLP) y algoritmos de Machine Learning, comparando diferentes técnicas de vectorización y modelos de clasificación para encontrar la solución óptima.

---

## 📊 Dataset

- **Fuente:** [SMS Spam Collection Dataset](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)
- **Total de mensajes:** 5,574
  - **Ham (legítimos):** 4,827 (86.6%)
  - **Spam:** 747 (13.4%)
- **Idioma:** Inglés
- **Formato:** Archivo de texto con formato `etiqueta\tmensaje`

### Distribución del Dataset

![Dataset Distribution](images/dataset_distribution.png)

---

## 🔧 Tecnologías Utilizadas

### Lenguaje y Librerías Principales

- **Python 3.8+**
- **Librerías de Machine Learning:**
  - `scikit-learn 1.3.0` - Modelos de ML y métricas
  - `nltk 3.8.1` - Procesamiento de lenguaje natural
- **Visualización y Análisis:**
  - `pandas 2.0.3` - Manipulación de datos
  - `numpy 1.24.3` - Operaciones numéricas
  - `matplotlib 3.7.0` - Gráficas
  - `seaborn 0.12.0` - Visualizaciones avanzadas

---

## 🚀 Características del Proyecto

### 1. Pipeline de Procesamiento de Texto (NLP)

El sistema implementa un pipeline completo de procesamiento:

```
Texto Original
    ↓
Eliminación de HTML tags
    ↓
Eliminación de URLs
    ↓
Tokenización
    ↓
Eliminación de Stopwords
    ↓
Eliminación de Puntuación
    ↓
Stemming (Porter Stemmer)
    ↓
Texto Procesado
```

**Ejemplo de procesamiento:**
```
Original: "Congratulations! You won a free iPhone. Click here now!"
Procesado: "congratul free iphon click"
```

### 2. Técnicas de Vectorización

- ✅ **TF-IDF Vectorizer** - Captura importancia de palabras únicas
- ✅ **Count Vectorizer** - Conteo simple de frecuencias

### 3. Modelos de Machine Learning Evaluados

| Modelo | Vectorización | Accuracy | Precision (Spam) | Recall (Spam) | F1-Score |
|--------|--------------|----------|------------------|---------------|----------|
| Logistic Regression | TF-IDF | 96.23% | 0.98 | 0.76 | 0.85 |
| Naive Bayes | TF-IDF | 97.22% | 1.00 | 0.81 | 0.89 |
| **SVM** ⭐ | **TF-IDF** | **98.21%** | **0.99** | **0.89** | **0.93** |
| Naive Bayes | Count | 97.94% | 0.91 | 0.96 | 0.93 |
| SVM | Count | 98.21% | 0.99 | 0.89 | 0.93 |

![Model Comparison](images/accuracy_comparison.png)

---

## 📈 Resultados del Modelo Ganador

### **SVM + TF-IDF - 98.21% Accuracy**

```
              precision    recall  f1-score   support

         ham       0.98      1.00      0.99       954
        spam       0.99      0.89      0.93       161

    accuracy                           0.98      1115
   macro avg       0.98      0.94      0.96      1115
weighted avg       0.98      0.98      0.98      1115
```

### Matriz de Confusión

![Confusion Matrix](images/confusion_matrix.png)

```
[[952   2]    ← 952 HAM correctos, 2 falsos positivos
 [ 18 143]]   ← 18 falsos negativos, 143 SPAM correctos
```

### Interpretación de Resultados

- ✅ **952/954 mensajes legítimos** detectados correctamente (99.8%)
- ✅ **143/161 spam** detectados correctamente (88.8%)
- ⚠️ **Solo 2 falsos positivos** - Mensajes legítimos marcados como spam (0.2%)
- ⚠️ **18 falsos negativos** - Spam no detectados (11.2%)

**El modelo prioriza NO molestar a usuarios legítimos (bajo FP) sobre detectar TODO el spam.**

---

## 💻 Instalación y Uso

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sms-spam-detection.git
cd sms-spam-detection
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar recursos de NLTK

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 5. Ejecutar el proyecto

```bash
# Entrenar modelo y generar visualizaciones
python procesamiento.py

# Generar solo visualizaciones
python visualizaciones.py

# Ejecutar demo interactivo (opcional)
streamlit run app.py
```

---

## 🎮 Uso del Modelo

### Predicción con Mensajes Nuevos

```python
import pickle
from procesamiento import SMSParser

# 1. Cargar modelo y vectorizador
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('svm_model.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Procesar y predecir
parser = SMSParser()
mensaje = "URGENT: Your account will be closed. Verify now!"

# 3. Pipeline completo
mensaje_procesado = parser.parse(mensaje)
mensaje_vectorizado = vectorizer.transform([mensaje_procesado]).toarray()
prediccion = model.predict(mensaje_vectorizado)[0]

print(f"Predicción: {prediccion}")  # Output: spam
```

### Ejemplo de Predicciones

```python
Mensaje: "Congratulations! You won a free iPhone. Click here now!"
Predicción: HAM (⚠️ Falso negativo - debería ser SPAM)

Mensaje: "Hey, are we still meeting for lunch tomorrow?"
Predicción: HAM ✅

Mensaje: "URGENT: Your account will be closed. Verify now!"
Predicción: SPAM ✅
```

---

## 🏗️ Arquitectura del Código

### Clases Principales

#### `HTMLStripper`
```python
class HTMLStripper(HTMLParser):
    """
    Elimina tags HTML del texto
    Ejemplo: "<p>Spam</p>" → "Spam"
    """
```

#### `SMSParser`
```python
class SMSParser:
    """
    Pipeline completo de procesamiento NLP
    
    Métodos:
    --------
    parse(mensaje) : str
        Procesa un mensaje completo
    
    strip_tags(mensaje) : str
        Elimina HTML
    
    remove_urls(mensaje) : str
        Elimina URLs
    
    clean_text(tokens) : list
        Limpia, elimina stopwords y aplica stemming
    
    crear_dataset(ruta, num) : tuple
        Procesa múltiples mensajes del dataset
    """
```

### Funciones de Visualización

```python
# visualizaciones.py

grafica_comparacion_modelos()      # Compara accuracy de todos los modelos
grafica_distribucion_dataset()     # Muestra distribución ham vs spam
grafica_metricas_detalladas()      # Precision, recall, f1-score
grafica_matriz_confusion(y, pred)  # Matriz de confusión del modelo
generar_todas_graficas(y, pred)    # Genera todas las gráficas
```

---

## 📊 Visualizaciones Generadas

El proyecto genera automáticamente 4 gráficas profesionales:

1. **`accuracy_comparison.png`** - Comparación de accuracy entre modelos
2. **`confusion_matrix.png`** - Matriz de confusión del mejor modelo
3. **`dataset_distribution.png`** - Distribución del dataset
4. **`metrics_comparison.png`** - Métricas detalladas por modelo

Todas se guardan en la carpeta `images/`

---

## 🎓 Aprendizajes Clave

### 1. TF-IDF vs Count Vectorizer

- **TF-IDF** funciona mejor con SVM porque:
  - Asigna mayor peso a palabras únicas del spam
  - Reduce el impacto de palabras comunes
  - Captura mejor la "importancia" de términos

### 2. Desbalance de Clases

Con 86% ham vs 14% spam, es crucial evaluar:
- ✅ **Precision y Recall** - No solo accuracy
- ✅ **Matriz de Confusión** - Entender tipos de errores
- ✅ **F1-Score** - Balance entre precision y recall

### 3. Trade-off Precision-Recall

El modelo prioriza:
- ✅ **Bajo Falsos Positivos** - No molestar usuarios legítimos
- ⚠️ **Mayor Falsos Negativos** - Algunos spam pasan

**En producción:** Este enfoque es mejor que marcar ham como spam.

### 4. Limitaciones del Modelo

- ⚠️ Entrenado solo con **SMS en inglés**
- ⚠️ No funciona igual con **spam de email moderno**
- ⚠️ Spam muy creativo puede evadir detección
- ⚠️ Requiere re-entrenamiento con nuevos patrones

---

## 🔮 Mejoras Futuras

### Técnicas Avanzadas
- [ ] Implementar validación cruzada (K-Fold)
- [ ] Probar Deep Learning (LSTM, BERT, Transformers)
- [ ] Manejo de desbalance de clases (SMOTE, class weights)
- [ ] Ensemble methods (Voting, Stacking)

### Ingeniería de Características
- [ ] N-gramas (bigrams, trigrams)
- [ ] Características adicionales (longitud, mayúsculas, números)
- [ ] Word embeddings (Word2Vec, GloVe)

### Deployment y Producción
- [ ] Crear API REST con Flask/FastAPI
- [ ] Deploy en cloud (AWS Lambda, Google Cloud)
- [ ] Contenedorización con Docker
- [ ] CI/CD pipeline con GitHub Actions
- [ ] Monitoreo de modelo en producción (MLOps)

### Interfaz de Usuario
- [ ] Aplicación web con Streamlit ✅ (en progreso)
- [ ] Integración con servicios de SMS
- [ ] Dashboard de métricas en tiempo real
- [ ] A/B testing de diferentes versiones

---

## 🌍 Casos de Uso Reales

### Empresas que Necesitan Esta Solución

1. **Telecomunicaciones** 📱
   - Movistar, Claro, AT&T, Verizon
   - Filtrar millones de SMS diariamente

2. **Email Providers** 📧
   - Gmail, Outlook, Yahoo
   - Adaptable para detección de spam en emails

3. **Apps de Mensajería** 💬
   - WhatsApp Business, Telegram
   - Moderación automática de mensajes

4. **Instituciones Financieras** 🏦
   - Bancos, fintech
   - Detectar mensajes fraudulentos/phishing

5. **E-commerce** 🛒
   - Amazon, MercadoLibre
   - Filtrar reviews falsas y spam

6. **Soporte al Cliente** 🎫
   - Call centers
   - Clasificar tickets automáticamente

### Aplicaciones Similares

Este mismo patrón se puede aplicar a:

- ✅ **Análisis de sentimientos** (reviews, redes sociales)
- ✅ **Detección de noticias falsas**
- ✅ **Clasificación de documentos**
- ✅ **Moderación de contenido**
- ✅ **Detección de intención** (chatbots)

---

## 💰 Valor Comercial

### Como Freelancer

**Plataformas:** Upwork, Fiverr, Freelancer.com, LinkedIn

**Servicios ofrecidos:**
- Implementación de filtros anti-spam personalizados
- Clasificadores de texto con Machine Learning
- Sistemas de análisis de sentimientos
- Automatización de clasificación de tickets

**Rango de precios:**
- Proyectos pequeños: $500 - $1,500 USD
- Proyectos empresariales: $3,000 - $10,000 USD

### Como Empleado

**Posiciones:**
- Machine Learning Engineer
- Data Scientist
- NLP Engineer
- AI/ML Developer

**Salarios aproximados (USD/año):**
- Junior: $40,000 - $60,000
- Mid-level: $80,000 - $120,000
- Senior: $120,000 - $180,000

---

## 📚 Recursos Adicionales

### Datasets para Practicar

- [Kaggle Datasets](https://www.kaggle.com/datasets) - Miles de datasets
- [UCI ML Repository](https://archive.ics.uci.edu/ml/) - Datasets académicos
- [HuggingFace](https://huggingface.co/datasets) - Datasets de NLP modernos
- [Google Dataset Search](https://datasetsearch.research.google.com/)

### Datasets Recomendados

- Amazon Reviews (sentiment analysis)
- IMDB Movie Reviews (sentiment)
- 20 Newsgroups (clasificación de documentos)
- Yelp Reviews (sentiment)
- Twitter Sentiment Analysis
- Fake News Detection

### Tutoriales y Documentación

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [NLTK Book](https://www.nltk.org/book/)
- [Real Python - NLP](https://realpython.com/nltk-nlp-python/)
- [Towards Data Science](https://towardsdatascience.com/)

---

## 👨‍💻 Autor

**[Tu Nombre]**

- 🌐 Portfolio: [tu-portfolio.com](https://tu-portfolio.com)
- 💼 LinkedIn: [linkedin.com/in/tu-perfil](https://linkedin.com/in/tu-perfil)
- 🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- 📧 Email: tu-email@example.com

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 [Tu Nombre]

Se concede permiso para usar, copiar, modificar y distribuir este software...
```

---

## 🙏 Agradecimientos

- Dataset: [UCI Machine Learning Repository - SMS Spam Collection](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)
- Inspiración: Proyectos de detección de spam en Kaggle
- Comunidad: Stack Overflow, Reddit r/MachineLearning

---

## 📞 Contacto y Soporte

¿Tienes preguntas o sugerencias? 

- 🐛 **Reportar bugs:** [GitHub Issues](https://github.com/tu-usuario/sms-spam-detection/issues)
- 💡 **Sugerencias:** [GitHub Discussions](https://github.com/tu-usuario/sms-spam-detection/discussions)
- 📧 **Email:** tu-email@example.com

---

## ⭐ Dale una Estrella

Si este proyecto te fue útil, ¡dale una ⭐ en GitHub! Ayuda a otros desarrolladores a encontrarlo.

---

## 📁 Estructura Completa del Proyecto



📁 sms-spam-detection/
│
├── 📄 README.md                      # ← Este archivo (documentación principal)
├── 📄 LICENSE                        # Licencia MIT
├── 📄 requirements.txt               # Dependencias del proyecto
├── 📄 .gitignore                     # Archivos a ignorar en Git
│
├── 📄 procesamiento.py               # ⭐ Script principal de entrenamiento
│   ├── Función: leer_correos()       # Lee dataset del archivo
│   ├── Clase: HTMLStripper           # Elimina tags HTML
│   ├── Clase: SMSParser              # Pipeline de NLP completo
│   ├── Entrenamiento de modelos      # Logistic, Naive Bayes, SVM
│   ├── Comparación TF-IDF vs Count   # Análisis de vectorización
│   └── Guardado de modelos           # Persistencia con pickle
│
├── 📄 visualizaciones.py             # 📊 Generación de gráficas
│   ├── grafica_comparacion_modelos() # Barra: accuracy de modelos
│   ├── grafica_matriz_confusion()    # Heatmap: matriz de confusión
│   ├── grafica_distribucion_dataset()# Pastel: ham vs spam
│   ├── grafica_metricas_detalladas() # Barra: precision/recall/f1
│   └── generar_todas_graficas()      # Ejecuta todas las gráficas
│
├── 📄 app.py                         # 🌐 Demo interactivo (Streamlit)
│   ├── Interfaz web                  # UI amigable para usuarios
│   ├── Carga de modelo               # Importa modelo guardado
│   ├── Predicción en tiempo real     # Clasifica mensajes nuevos
│   └── Visualización de resultados   # Muestra HAM o SPAM
│
├── 📄 tfidf_vectorizer.pkl           # 💾 Vectorizador TF-IDF guardado
├── 📄 svm_model.pkl                  # 💾 Modelo SVM entrenado guardado
│
├── 📁 smspamcoll/                    # 📂 Carpeta del dataset
│   └── 📄 SMSSpamCollection          # Archivo original del dataset
│       ├── Formato: etiqueta\tmensaje
│       ├── Total: 5,574 mensajes
│       ├── Ham: 4,827 (86.6%)
│       └── Spam: 747 (13.4%)
│
├── 📁 images/                        # 📂 Gráficas generadas (auto-creada)
│   ├── 📊 accuracy_comparison.png    # Comparación de modelos
│   ├── 📊 confusion_matrix.png       # Matriz de confusión SVM
│   ├── 📊 dataset_distribution.png   # Distribución del dataset
│   └── 📊 metrics_comparison.png     # Métricas detalladas
│
├── 📁 docs/                          # 📂 Documentación adicional (opcional)
│   ├── 📄 technical_guide.md         # Guía técnica detallada
│   ├── 📄 deployment_guide.md        # Guía de despliegue
│   └── 📄 api_documentation.md       # Documentación de API (si existe)
│
├── 📁 tests/                         # 📂 Tests unitarios (opcional)
│   ├── 📄 test_parser.py             # Tests para SMSParser
│   ├── 📄 test_model.py              # Tests para predicciones
│   └── 📄 test_visualizations.py     # Tests para gráficas
│
└── 📁 notebooks/                     # 📂 Jupyter Notebooks (opcional)
    ├── 📓 exploratory_analysis.ipynb # Análisis exploratorio
    ├── 📓 model_comparison.ipynb     # Comparación de modelos
    └── 📓 feature_engineering.ipynb  # Ingeniería de características
```

---

### 📋 Descripción Detallada de Archivos

#### Archivos Principales

| Archivo | Líneas | Descripción | Uso |
|---------|--------|-------------|-----|
| `procesamiento.py` | ~400 | Script principal completo | `python procesamiento.py` |
| `visualizaciones.py` | ~200 | Generador de gráficas | `python visualizaciones.py` |
| `app.py` | ~100 | Demo web interactivo | `streamlit run app.py` |

#### Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `requirements.txt` | Lista de dependencias para `pip install` |
| `.gitignore` | Archivos/carpetas excluidos del repositorio |
| `LICENSE` | Términos de uso (MIT License) |

#### Modelos Guardados

| Archivo | Tamaño aprox. | Contenido |
|---------|---------------|-----------|
| `tfidf_vectorizer.pkl` | ~500 KB | Vocabulario y pesos TF-IDF de 7,453 palabras |
| `svm_model.pkl` | ~2 MB | Modelo SVM entrenado con 4,459 ejemplos |

#### Dataset

```
📄 SMSSpamCollection (formato)
---------------------------------
ham    Go until jurong point, crazy.. Available only...
spam   Free entry in 2 a wkly comp to win FA Cup...
ham    U dun say so early hor... U c already then say...
spam   FreeMsg Hey there darling it's been 3 week's...
```

---

### 🔄 Flujo de Ejecución

```
1. ENTRENAMIENTO (procesamiento.py)
   ↓
   Leer dataset → Procesar texto (NLP) → Vectorizar (TF-IDF)
   ↓
   Train/Test Split → Entrenar modelos → Evaluar métricas
   ↓
   Guardar mejor modelo (SVM) → Generar visualizaciones
   ↓
   Archivos creados: svm_model.pkl, tfidf_vectorizer.pkl, images/

2. VISUALIZACIÓN (visualizaciones.py)
   ↓
   Leer métricas → Generar gráficas → Guardar en images/

3. PREDICCIÓN (app.py o código custom)
   ↓
   Cargar modelo → Procesar mensaje nuevo → Predecir → Mostrar resultado
```

---

### 🎨 Personalización del Proyecto

Para adaptar el proyecto a tus necesidades:

```python
# 1. Cambiar dataset
x, y = parser.crear_dataset('tu_dataset.txt', num_mensajes)

# 2. Cambiar idioma (stopwords)
# En SMSParser.clean_text():
stopwords.words('spanish')  # o 'french', 'german', etc.

# 3. Ajustar hiperparámetros
clf_svm = SVC(kernel='rbf', C=10, gamma='scale')  # Diferentes parámetros

# 4. Probar otros modelos
from sklearn.ensemble import RandomForestClassifier
clf_rf = RandomForestClassifier(n_estimators=100)
```

---

### 📦 Contenido de `requirements.txt`

```txt
# Machine Learning y NLP
scikit-learn>=1.3.0
nltk>=3.8.1

# Manipulación de datos
pandas>=2.0.3
numpy>=1.24.3

# Visualización
matplotlib>=3.7.0
seaborn>=0.12.0

# Web app (opcional)
streamlit>=1.28.0

# Utilidades
pickle-mixin>=1.0.2
```

---

### 🚀 Comandos Rápidos

```bash
# Setup inicial
git clone https://github.com/tu-usuario/sms-spam-detection.git
cd sms-spam-detection
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Entrenar modelo
python procesamiento.py

# Generar solo gráficas
python visualizaciones.py

# Demo web
streamlit run app.py

# Tests (si existen)
pytest tests/
```

---

## 🎯 Checklist para Portafolio

- [x] Código limpio y comentado
- [x] README.md profesional
- [x] Visualizaciones de calidad
- [x] Modelos guardados funcionando
- [ ] Demo web con Streamlit
- [ ] Tests unitarios
- [ ] Documentación técnica adicional
- [ ] Video demo en YouTube
- [ ] Artículo en Medium/Dev.to
- [ ] Deploy en cloud (Heroku/AWS)

---

**Made with ❤️ and ☕ by [Tu Nombre]**

*Última actualización: Diciembre 2024*

---