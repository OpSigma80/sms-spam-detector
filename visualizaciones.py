"""
Visualizaciones del proyecto SMS Spam Detection
Genera gráficas profesionales para análisis y presentación
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import os

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Crear carpeta para imágenes si no existe
if not os.path.exists('images'):
    os.makedirs('images')

def grafica_comparacion_modelos():
    """Gráfica de barras comparando accuracy de todos los modelos"""
    
    modelos = ['Logistic\nRegression', 'Naive Bayes\n(TF-IDF)', 'SVM\n(TF-IDF)', 
               'Naive Bayes\n(Count)', 'SVM\n(Count)']
    accuracy = [96.23, 97.22, 98.21, 97.94, 98.21]
    
    plt.figure(figsize=(12, 7))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    bars = plt.bar(modelos, accuracy, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Agregar valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.2f}%', ha='center', va='bottom', 
                 fontsize=12, fontweight='bold')
    
    plt.ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
    plt.xlabel('Modelos', fontsize=13, fontweight='bold')
    plt.title('Comparación de Accuracy entre Modelos de Clasificación', 
              fontsize=15, fontweight='bold', pad=20)
    plt.ylim(95, 99.5)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Guardar
    plt.savefig('images/accuracy_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica guardada: images/accuracy_comparison.png")
    plt.show()


def grafica_matriz_confusion(y_test, y_pred):
    """Matriz de confusión del mejor modelo (SVM + TF-IDF)"""
    
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['HAM', 'SPAM'], 
                yticklabels=['HAM', 'SPAM'],
                cbar_kws={'label': 'Cantidad'},
                annot_kws={'size': 16, 'weight': 'bold'},
                linewidths=2, linecolor='black')
    
    plt.ylabel('Etiqueta Real', fontsize=13, fontweight='bold')
    plt.xlabel('Predicción del Modelo', fontsize=13, fontweight='bold')
    plt.title('Matriz de Confusión - SVM + TF-IDF (98.21% Accuracy)', 
              fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    
    # Guardar
    plt.savefig('images/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica guardada: images/confusion_matrix.png")
    plt.show()


def grafica_distribucion_dataset():
    """Gráfica de pastel mostrando distribución HAM vs SPAM"""
    
    labels = ['HAM (Legítimo)', 'SPAM']
    sizes = [4827, 747]
    colors = ['#4ECDC4', '#FF6B6B']
    explode = (0.05, 0.1)
    
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, 
                                        colors=colors, autopct='%1.1f%%', 
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': 13, 'weight': 'bold'})
    
    # Mejorar estilo de porcentajes
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
    
    plt.title('Distribución del Dataset SMS Spam Collection\n(Total: 5,574 mensajes)', 
              fontsize=15, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    
    # Guardar
    plt.savefig('images/dataset_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica guardada: images/dataset_distribution.png")
    plt.show()


def grafica_metricas_detalladas():
    """Gráfica comparando precision, recall y f1-score"""
    
    modelos = ['Logistic\nRegression', 'Naive Bayes', 'SVM']
    precision_ham = [0.96, 0.97, 0.98]
    recall_ham = [1.00, 1.00, 1.00]
    precision_spam = [0.98, 1.00, 0.99]
    recall_spam = [0.76, 0.81, 0.89]
    
    x = np.arange(len(modelos))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars1 = ax.bar(x - width*1.5, precision_ham, width, label='Precision HAM', 
                   color='#4ECDC4', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x - width/2, recall_ham, width, label='Recall HAM', 
                   color='#95E1D3', edgecolor='black', linewidth=1.2)
    bars3 = ax.bar(x + width/2, precision_spam, width, label='Precision SPAM', 
                   color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars4 = ax.bar(x + width*1.5, recall_spam, width, label='Recall SPAM', 
                   color='#FFA07A', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Score', fontsize=13, fontweight='bold')
    ax.set_xlabel('Modelos (TF-IDF)', fontsize=13, fontweight='bold')
    ax.set_title('Comparación de Métricas por Modelo', fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(modelos)
    ax.legend(loc='lower right', fontsize=11)
    ax.set_ylim(0.7, 1.05)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('images/metrics_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica guardada: images/metrics_comparison.png")
    plt.show()


# Función principal para generar todas las gráficas
def generar_todas_graficas(y_test=None, y_pred=None):
    """Genera todas las visualizaciones del proyecto"""
    
    print("\n" + "="*50)
    print("GENERANDO VISUALIZACIONES")
    print("="*50 + "\n")
    
    # 1. Comparación de modelos
    grafica_comparacion_modelos()
    
    # 2. Distribución del dataset
    grafica_distribucion_dataset()
    
    # 3. Métricas detalladas
    grafica_metricas_detalladas()
    
    # 4. Matriz de confusión (si se proporcionan datos)
    if y_test is not None and y_pred is not None:
        grafica_matriz_confusion(y_test, y_pred)
    else:
        print("⚠️  Para generar la matriz de confusión, pasa y_test y y_pred como parámetros")
    
    print("\n" + "="*50)
    print("✓ TODAS LAS GRÁFICAS GENERADAS EXITOSAMENTE")
    print("✓ Revisa la carpeta 'images/'")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Si ejecutas este archivo directamente, genera todas las gráficas
    generar_todas_graficas()
    
    # Para incluir matriz de confusión, descomenta y agrega tus datos:
    # from procesamiento import ... (importa tus datos de test)
    # generar_todas_graficas(y_test, y_pred_svm)