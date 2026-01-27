"""
Pruebas de Integración para el modelo

Estas pruebas verifican que los componentes funcionen correctamente juntos:
- Carga de modelos
- Pipeline completo de clasificación
- Guardado y recuperación de modelos
"""

import pytest
import sys
import os
import pickle

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCargaModelos:
    """Pruebas para carga de modelos guardados"""
    
    def test_modelo_svm_existe(self):
        """Verifica que el archivo del modelo SVM exista"""
        modelo_path = os.path.join(os.path.dirname(__file__), '..', 'svm_model.pkl')
        assert os.path.exists(modelo_path), "El archivo svm_model.pkl no existe"
    
    def test_vectorizador_existe(self):
        """Verifica que el archivo del vectorizador exista"""
        vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'tfidf_vectorizer.pkl')
        assert os.path.exists(vectorizer_path), "El archivo tfidf_vectorizer.pkl no existe"
    
    def test_cargar_modelo_svm(self):
        """Verifica que el modelo SVM se pueda cargar correctamente"""
        modelo_path = os.path.join(os.path.dirname(__file__), '..', 'svm_model.pkl')
        
        if os.path.exists(modelo_path):
            with open(modelo_path, 'rb') as f:
                modelo = pickle.load(f)
            
            # Verificar que el modelo tiene el método predict
            assert hasattr(modelo, 'predict'), "El modelo no tiene método predict"
            assert True
        else:
            pytest.skip("Modelo no encontrado - ejecuta procesamiento.py primero")
    
    def test_cargar_vectorizador(self):
        """Verifica que el vectorizador se pueda cargar correctamente"""
        vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'tfidf_vectorizer.pkl')
        
        if os.path.exists(vectorizer_path):
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            
            # Verificar que tiene el método transform
            assert hasattr(vectorizer, 'transform'), "El vectorizador no tiene método transform"
            assert True
        else:
            pytest.skip("Vectorizador no encontrado - ejecuta procesamiento.py primero")


class TestPipelineCompleto:
    """Pruebas del pipeline completo de clasificación"""
    
    @pytest.fixture
    def cargar_componentes(self):
        """Fixture para cargar modelo y vectorizador"""
        modelo_path = os.path.join(os.path.dirname(__file__), '..', 'svm_model.pkl')
        vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'tfidf_vectorizer.pkl')
        
        if not (os.path.exists(modelo_path) and os.path.exists(vectorizer_path)):
            pytest.skip("Modelos no encontrados - ejecuta procesamiento.py primero")
        
        with open(modelo_path, 'rb') as f:
            modelo = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        return modelo, vectorizer
    
    def test_prediccion_mensaje_spam(self, cargar_componentes):
        """Verifica predicción de mensaje spam obvio"""
        modelo, vectorizer = cargar_componentes
        
        # Mensaje claramente spam
        mensaje_spam = "FREE PRIZE!!! Call NOW to WIN $1000 GUARANTEED"
        
        # Vectorizar y predecir
        vector = vectorizer.transform([mensaje_spam])
        # Convertir sparse a dense si es necesario
        if hasattr(vector, 'toarray'):
            vector = vector.toarray()
        prediccion = modelo.predict(vector)
        
        # Verificar que la predicción sea válida
        assert prediccion[0] in ['spam', 'ham', 0, 1], "Predicción no válida"
        assert True
    
    def test_prediccion_mensaje_normal(self, cargar_componentes):
        """Verifica predicción de mensaje normal"""
        modelo, vectorizer = cargar_componentes
        
        # Mensaje claramente normal
        mensaje_normal = "Hola, nos vemos mañana en la oficina"
        
        # Vectorizar y predecir
        vector = vectorizer.transform([mensaje_normal])
        # Convertir sparse a dense si es necesario
        if hasattr(vector, 'toarray'):
            vector = vector.toarray()
        prediccion = modelo.predict(vector)
        
        # Verificar que la predicción sea válida
        assert prediccion[0] in ['spam', 'ham', 0, 1], "Predicción no válida"
        assert True
    
    def test_prediccion_batch(self, cargar_componentes):
        """Verifica predicción de múltiples mensajes"""
        modelo, vectorizer = cargar_componentes
        
        mensajes = [
            "FREE PRIZE!!!",
            "Hola mamá",
            "URGENT: Click here NOW",
            "Nos vemos el lunes"
        ]
        
        # Vectorizar y predecir
        vectores = vectorizer.transform(mensajes)
        # Convertir sparse a dense si es necesario
        if hasattr(vectores, 'toarray'):
            vectores = vectores.toarray()
        predicciones = modelo.predict(vectores)
        
        # Verificar que devuelve el número correcto de predicciones
        assert len(predicciones) == len(mensajes), "Número incorrecto de predicciones"
        assert True
    
    def test_consistencia_predicciones(self, cargar_componentes):
        """Verifica que predicciones sean consistentes"""
        modelo, vectorizer = cargar_componentes
        
        mensaje = "FREE MONEY NOW"
        
        # Hacer la misma predicción dos veces
        vector1 = vectorizer.transform([mensaje])
        if hasattr(vector1, 'toarray'):
            vector1 = vector1.toarray()
        pred1 = modelo.predict(vector1)
        
        vector2 = vectorizer.transform([mensaje])
        if hasattr(vector2, 'toarray'):
            vector2 = vector2.toarray()
        pred2 = modelo.predict(vector2)
        
        # Deben ser iguales
        assert pred1[0] == pred2[0], "Las predicciones no son consistentes"


class TestRendimiento:
    """Pruebas de rendimiento del modelo"""
    
    @pytest.fixture
    def cargar_componentes(self):
        """Fixture para cargar modelo y vectorizador"""
        modelo_path = os.path.join(os.path.dirname(__file__), '..', 'svm_model.pkl')
        vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'tfidf_vectorizer.pkl')
        
        if not (os.path.exists(modelo_path) and os.path.exists(vectorizer_path)):
            pytest.skip("Modelos no encontrados")
        
        with open(modelo_path, 'rb') as f:
            modelo = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        return modelo, vectorizer
    
    def test_velocidad_prediccion(self, cargar_componentes):
        """Verifica que las predicciones sean rápidas"""
        import time
        
        modelo, vectorizer = cargar_componentes
        mensaje = "Este es un mensaje de prueba"
        
        # Medir tiempo
        inicio = time.time()
        vector = vectorizer.transform([mensaje])
        if hasattr(vector, 'toarray'):
            vector = vector.toarray()
        modelo.predict(vector)
        duracion = time.time() - inicio
        
        # Debe ser menor a 100ms
        assert duracion < 0.1, f"Predicción muy lenta: {duracion:.3f}s"


# Ejecutar solo este archivo
if __name__ == "__main__":
    pytest.main([__file__, "-v"])