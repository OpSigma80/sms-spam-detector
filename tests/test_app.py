"""
Pruebas para la aplicación Flask (app.py)

Estas pruebas verifican que los endpoints de la aplicación web
funcionen correctamente.
"""

import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Intentar importar la app Flask
try:
    from app import app
    APP_DISPONIBLE = True
except ImportError:
    APP_DISPONIBLE = False


@pytest.mark.skipif(not APP_DISPONIBLE, reason="app.py no disponible")
class TestFlaskApp:
    """Pruebas para la aplicación Flask"""
    
    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_homepage_exists(self, client):
        """Verifica que la página principal exista"""
        response = client.get('/')
        assert response.status_code == 200, "La página principal no responde"
    
    def test_homepage_content(self, client):
        """Verifica que la página principal tenga contenido"""
        response = client.get('/')
        assert response.data is not None, "La página no tiene contenido"
        assert len(response.data) > 0, "La página está vacía"


@pytest.mark.skipif(not APP_DISPONIBLE, reason="app.py no disponible")
class TestAPIEndpoints:
    """Pruebas para endpoints de la API (si existen)"""
    
    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_predict_endpoint_exists(self, client):
        """Verifica que el endpoint de predicción exista"""
        # Ajusta la ruta según tu aplicación
        # response = client.post('/predict', json={'mensaje': 'test'})
        # Esto es un placeholder - ajústalo según tu código
        assert True  # Placeholder
    
    def test_predict_with_spam_message(self, client):
        """Prueba predicción de mensaje spam"""
        # Ejemplo de prueba - ajústalo según tu API
        # response = client.post('/predict', json={
        #     'mensaje': 'FREE PRIZE WIN NOW'
        # })
        # assert response.status_code == 200
        # data = response.get_json()
        # assert 'prediccion' in data
        assert True  # Placeholder
    
    def test_predict_with_normal_message(self, client):
        """Prueba predicción de mensaje normal"""
        # response = client.post('/predict', json={
        #     'mensaje': 'Hola, ¿cómo estás?'
        # })
        # assert response.status_code == 200
        assert True  # Placeholder
    
    def test_predict_with_empty_message(self, client):
        """Verifica manejo de mensaje vacío"""
        # response = client.post('/predict', json={'mensaje': ''})
        # Debería devolver error o manejo apropiado
        assert True  # Placeholder
    
    def test_predict_without_message(self, client):
        """Verifica manejo de request sin mensaje"""
        # response = client.post('/predict', json={})
        # assert response.status_code in [400, 422]  # Bad request
        assert True  # Placeholder


@pytest.mark.skipif(not APP_DISPONIBLE, reason="app.py no disponible")
class TestErrorHandling:
    """Pruebas de manejo de errores"""
    
    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_404_error(self, client):
        """Verifica manejo de página no encontrada"""
        response = client.get('/pagina-que-no-existe')
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Verifica manejo de método HTTP incorrecto"""
        # Si tu endpoint solo acepta POST
        # response = client.get('/predict')
        # assert response.status_code == 405  # Method not allowed
        assert True  # Placeholder


# Pruebas que no requieren la app
class TestAppStructure:
    """Pruebas de estructura sin ejecutar la app"""
    
    def test_app_file_exists(self):
        """Verifica que app.py exista"""
        app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
        assert os.path.exists(app_path), "app.py no existe"
    
    def test_templates_folder_exists(self):
        """Verifica que exista carpeta de templates"""
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        # Este es opcional - ajusta según tu estructura
        # assert os.path.exists(templates_path), "Carpeta templates no existe"
        assert True  # Placeholder
    
    def test_static_folder_exists(self):
        """Verifica que exista carpeta de archivos estáticos"""
        static_path = os.path.join(os.path.dirname(__file__), '..', 'static')
        # Este es opcional - ajusta según tu estructura
        # assert os.path.exists(static_path), "Carpeta static no existe"
        assert True  # Placeholder


# Ejecutar solo este archivo
if __name__ == "__main__":
    pytest.main([__file__, "-v"])