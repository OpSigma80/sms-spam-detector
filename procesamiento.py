
import nltk
import string
import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk import PorterStemmer
from nltk.corpus import stopwords
from html.parser import HTMLParser 
from visualizaciones import generar_todas_graficas



def leer_correos(ruta_archivo, num):
    # La variable 'ruta_archivo' es la misma que 'indice' que usaste
    
    X = []  # Para los mensajes (texto)
    Y = []  # Para las etiquetas (ham/spam)
    
    try:
        with open(ruta_archivo, 'r', encoding='latin-1') as f:
            # Iterar sobre las líneas del archivo
            for i, linea in enumerate(f):
                if i >= num:
                    break  # Detenerse después de 'num' líneas

                # El archivo SMSSpamCollection usa '\t' (tabulador) como separador
                # Usamos .strip() para eliminar los saltos de línea al final
                partes = linea.strip().split('\t')
                
                # Asegurarse de que la línea tiene dos partes (etiqueta y mensaje)
                if len(partes) == 2:
                    etiqueta = partes[0]  # 'ham' o 'spam'
                    mensaje = partes[1]   # El texto completo del SMS
                    
                    Y.append(etiqueta)
                    X.append(mensaje)

        return X, Y
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
        return [], []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return [], []

# Prueba tu función con las primeras 10 líneas
X, Y = leer_correos('smspamcoll/SMSSpamCollection', 10)

print(f"Total de registros leídos: {len(Y)}")
if Y:
    print("\nEtiqueta del primer registro (Y[0]):") 
    print(Y[0]) 
    print("\nMensaje del primer registro (X[0]):")
    print(X[0])
    
class HTMLStripper(HTMLParser):
    """Clase auxiliar para eliminar tags HTML"""
    def __init__(self):
        super().__init__()
        self.d = []
    
    def handle_data(self, d):
        self.d.append(d)

class SMSParser:
    """Parser para limpiar y procesar mensajes SMS"""
   
   
    def parse(self, mensaje):
        """Aplica todas las transformaciones al mensaje"""
        # Eliminamos tags HTML (por seguridad)
        pmensaje = self.strip_tags(mensaje)
        # Eliminamos URLs
        pmensaje = self.remove_urls(pmensaje)
        # Tokenizamos
        pmensaje = word_tokenize(pmensaje)
        # Limpiamos y aplicamos stemming
        pmensaje = self.clean_text(pmensaje)
        return " ".join(pmensaje)
           
       
    def strip_tags(self, mensaje):
        """Elimina tags HTML si existen"""
        html_stripper = HTMLStripper()
        html_stripper.feed(mensaje)
        return ''.join(html_stripper.d) if html_stripper.d else mensaje
    
    def remove_urls(self, mensaje):
        return re.sub(r"http\S+", "", mensaje)

    def clean_text(self, mensaje):
        pmensaje = []
        st = PorterStemmer()
        punct = list(punctuation) + ["\n", "\t", "=", "/","..","..."]
        for word in mensaje:
            if word not in stopwords.words('english') and word not in punct:
                # Aplicamos stemming
                pmensaje.append(st.stem(word))
        return pmensaje
            
        
       

    def crear_dataset(self, ruta_archivo, num):
        mensajes_parser = SMSParser()
        x, y = leer_correos(ruta_archivo, num)
        x_proc = []
        for i, mensaje in enumerate(x):
             print("\rParsing mensaje: {}".format(i+1), end='')
             x_proc.append(mensajes_parser.parse(mensaje))
        print()
        return x_proc, y
  
parser = SMSParser()
result = parser.parse(X[0])        
print(result)

x, y = parser.crear_dataset('smspamcoll/SMSSpamCollection',  5574)
print(x[50])

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
# Entrenar con TODOS los mensajes

#vectorizer = CountVectorizer()
#vectorizer.fit(x)  # <-- Todos los mensajes procesados


# Reemplaza CountVectorizer por TfidfVectorizer
vectorizer = TfidfVectorizer()
x_vect = vectorizer.fit_transform(x)

#clf = MultinomialNB()
#clf.fit(X_train, y_train)

#clf = SVC(kernel='linear')
#clf.fit(X_train, y_train)


# Ver las palabras del vocabulario
print("Total de palabras únicas:", len(vectorizer.get_feature_names_out()))

# Transformar todos los mensajes
x_vect = vectorizer.transform(x)
print("Tipo de x_vect:", type(x_vect))
print("Shape de la matriz:", x_vect.shape)


# CONVIERTE TODO A ARRAY PRIMERO
x_array = x_vect.toarray() # type: ignore

# Ahora sí funciona todo
print("\nPrimeros 3 mensajes vectorizados:")
print(x_array[:3])

print("\nPrimer mensaje:")
print(x_array[0])

# Ver palabras del primer mensaje
palabras = vectorizer.get_feature_names_out()
vector_primer_mensaje = x_array[0]

print("\nPalabras presentes en el primer mensaje:")
for i, freq in enumerate(vector_primer_mensaje):
    if freq > 0:
        print(f"{palabras[i]}: {int(freq)}")

df = pd.DataFrame(x_vect.toarray(), columns=[vectorizer.get_feature_names_out()]) # type: ignore
df['etiqueta'] = y
print(df.head())
print(f"\nShape del DataFrame: {df.shape}")
print(df['etiqueta'].value_counts())
clf = LogisticRegression()
print("\nEntrenando el modelo...")
clf.fit(x_vect, y)
print("Modelo entrenado.")
print("\nProbando el modelo con un nuevo mensaje...")


# 1. Dividir en train y test
X_train, X_test, y_train, y_test = train_test_split(
    x_vect.toarray(),  # o x_array si ya lo convertiste # type: ignore
    y, 
    test_size=0.2,     # 20% para test
    random_state=42    # Para reproducibilidad
)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# 2. Crear y entrenar el modelo
clf = LogisticRegression(max_iter=1000)  # max_iter para que converja
clf.fit(X_train, y_train)

# 3. Hacer predicciones
y_pred = clf.predict(X_test)

print("\n========== LOGISTIC REGRESSION ==========")
# 4. Evaluar el modelo
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

# ========== NAIVE BAYES ==========
print("\n========== NAIVE BAYES ==========")
clf_nb = MultinomialNB()
clf_nb.fit(X_train, y_train)
y_pred_nb = clf_nb.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred_nb))
print("\nReporte:")
print(classification_report(y_test, y_pred_nb))
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred_nb))

# ========== SVM ==========
print("\n========== SVM ==========")
clf_svm = SVC(kernel='linear')
clf_svm.fit(X_train, y_train)
y_pred_svm = clf_svm.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred_svm))
print("\nReporte:")
print(classification_report(y_test, y_pred_svm))
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred_svm))

from sklearn.feature_extraction.text import CountVectorizer

print("\n" + "="*50)
print("PROBANDO CON CountVectorizer")
print("="*50)

# Vectorización con CountVectorizer
vectorizer_count = CountVectorizer()
x_vect_count = vectorizer_count.fit_transform(x)

print(f"Shape de la matriz: {x_vect_count.shape}")

# División train/test
X_train_count, X_test_count, y_train_count, y_test_count = train_test_split(
    x_vect_count.toarray(),  # type: ignore
    y, 
    test_size=0.2,
    random_state=42
)

# ========== NAIVE BAYES con CountVectorizer ==========
print("\n========== NAIVE BAYES + CountVectorizer ==========")
clf_nb_count = MultinomialNB()
clf_nb_count.fit(X_train_count, y_train_count)
y_pred_nb_count = clf_nb_count.predict(X_test_count)

print("Accuracy:", accuracy_score(y_test_count, y_pred_nb_count))
print("\nReporte:")
print(classification_report(y_test_count, y_pred_nb_count))
print("Matriz de confusión:")
print(confusion_matrix(y_test_count, y_pred_nb_count))

# ========== SVM con CountVectorizer ==========
print("\n========== SVM + CountVectorizer ==========")
clf_svm_count = SVC(kernel='linear')
clf_svm_count.fit(X_train_count, y_train_count)
y_pred_svm_count = clf_svm_count.predict(X_test_count)

print("Accuracy:", accuracy_score(y_test_count, y_pred_svm_count))
print("\nReporte:")
print(classification_report(y_test_count, y_pred_svm_count))
print("Matriz de confusión:")
print(confusion_matrix(y_test_count, y_pred_svm_count))

import pickle

# Guardar el modelo SVM y el vectorizador TF-IDF
print("\n========== GUARDANDO MODELO ==========")

# Guardar vectorizador
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("✓ Vectorizador guardado: tfidf_vectorizer.pkl")

# Guardar modelo SVM
with open('svm_model.pkl', 'wb') as f:
    pickle.dump(clf_svm, f)
print("✓ Modelo guardado: svm_model.pkl")

print("\n========== ANÁLISIS DE PROCESAMIENTO ==========")
mensajes_prueba = [
    "Congratulations! You won a free iPhone. Click here now!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT: Your account will be closed. Verify now!"
]
parser_test = SMSParser()
for msg in mensajes_prueba:
    msg_procesado = parser_test.parse(msg)
    print(f"\nOriginal: {msg}")
    print(f"Procesado: {msg_procesado}")



print("\n========== PROBANDO MODELO GUARDADO ==========")

# Cargar modelo y hacer predicción
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer_loaded = pickle.load(f)

with open('svm_model.pkl', 'rb') as f:
    model_loaded = pickle.load(f)

# Probar con mensajes nuevos
mensajes_prueba = [
    "Congratulations! You won a free iPhone. Click here now!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT: Your account will be closed. Verify now!"
]

parser_test = SMSParser()

print("\nPredicciones en mensajes nuevos:")
for msg in mensajes_prueba:
    # Procesar mensaje
    msg_procesado = parser_test.parse(msg)
    # Vectorizar
    msg_vectorizado = vectorizer_loaded.transform([msg_procesado])
    # Predecir (CONVERTIR A ARRAY DENSO)
    prediccion = model_loaded.predict(msg_vectorizado.toarray())[0]  # <-- Agregado .toarray()
    
    print(f"\nMensaje: {msg}")
    print(f"Predicción: {prediccion.upper()}")
    

# ========== GENERAR VISUALIZACIONES ==========
print("\n========== GENERANDO VISUALIZACIONES ==========")

from visualizaciones import (
    grafica_comparacion_modelos,
    grafica_distribucion_dataset,
    grafica_metricas_detalladas,
    grafica_matriz_confusion
)

# Generar todas las gráficas
grafica_comparacion_modelos()
grafica_distribucion_dataset()
grafica_metricas_detalladas()

# Matriz de confusión con datos reales del modelo SVM
grafica_matriz_confusion(y_test, y_pred_svm)

print("\n✓ Todas las visualizaciones generadas en la carpeta 'images/'")   

# Generar gráficas con los datos del modelo SVM
generar_todas_graficas(y_test, y_pred_svm)