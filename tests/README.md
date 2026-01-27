# 🧪 Tests - Guía de Pruebas

## 📋 Contenido

Este directorio contiene todas las pruebas automatizadas del proyecto.

### Archivos:

- **`test_preprocessing.py`** - Pruebas unitarias de funciones de preprocesamiento
- **`test_model.py`** - Pruebas de integración del modelo y pipeline
- **`test_app.py`** - Pruebas de la aplicación Flask

---

## 🚀 Cómo Ejecutar las Pruebas

### Opción 1: Ejecutar TODAS las pruebas

```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar todas las pruebas
pytest tests/ -v
```

O simplemente usa el script:
```bash
run_tests.bat
```

### Opción 2: Ejecutar archivo específico

```bash
# Solo pruebas del modelo
pytest tests/test_model.py -v

# Solo pruebas de preprocesamiento
pytest tests/test_preprocessing.py -v

# Solo pruebas de la app
pytest tests/test_app.py -v
```

### Opción 3: Ejecutar una prueba específica

```bash
pytest tests/test_model.py::TestCargaModelos::test_modelo_svm_existe -v
```

---

## 📊 Ver Cobertura de Código

```bash
# Ejecutar con reporte de cobertura
pytest --cov=. --cov-report=html

# Abrir reporte en el navegador
start htmlcov\index.html
```

---

## 🎯 Tipos de Pruebas

### 1. Pruebas Unitarias (`test_preprocessing.py`)
- Prueban funciones individuales
- No requieren dependencias externas
- Muy rápidas

### 2. Pruebas de Integración (`test_model.py`)
- Prueban componentes trabajando juntos
- Cargan modelos reales
- Verifican el pipeline completo

### 3. Pruebas de API (`test_app.py`)
- Prueban endpoints de Flask
- Verifican respuestas HTTP
- Simulan requests de usuarios

---

## ✅ Estado Actual

Las pruebas están configuradas con **placeholders** (marcadores).

**IMPORTANTE:** Necesitas personalizar las pruebas según tu código real:

1. Abre cada archivo `test_*.py`
2. Busca los comentarios con `# Placeholder`
3. Reemplaza con tu código real
4. Elimina los `assert True` temporales

---

## 🔧 Personalizar las Pruebas

### Ejemplo: Personalizar test_preprocessing.py

```python
# ❌ ANTES (Placeholder)
def test_texto_minusculas(self):
    assert True  # Placeholder

# ✅ DESPUÉS (Real)
def test_texto_minusculas(self):
    from procesamiento import limpiar_texto
    resultado = limpiar_texto("HOLA MUNDO")
    assert resultado == "hola mundo"
```

---

## 📝 Agregar Nuevas Pruebas

### Template para nueva prueba:

```python
def test_mi_nueva_funcionalidad(self):
    """Descripción de qué estás probando"""
    # 1. Preparar (Arrange)
    entrada = "datos de prueba"
    
    # 2. Ejecutar (Act)
    resultado = mi_funcion(entrada)
    
    # 3. Verificar (Assert)
    assert resultado == "resultado esperado"
```

---

## 🐛 Debugging de Pruebas

### Ver más detalles cuando falla:

```bash
# Mostrar print statements
pytest -v -s

# Mostrar traceback completo
pytest -v --tb=long

# Detener en el primer fallo
pytest -x

# Ejecutar solo pruebas que fallaron
pytest --lf
```

---

## 🎓 Buenas Prácticas

✅ **Hacer:**
- Escribir pruebas descriptivas
- Una prueba = una funcionalidad
- Usar nombres claros (`test_nombre_descriptivo`)
- Mantener pruebas independientes

❌ **Evitar:**
- Pruebas que dependen de otras pruebas
- Pruebas muy largas y complejas
- Hardcodear valores específicos del sistema

---

## 📚 Recursos

- [Documentación pytest](https://docs.pytest.org/)
- [Guía de Testing en Python](https://realpython.com/pytest-python-testing/)

---

## 🆘 Problemas Comunes

### Error: "ModuleNotFoundError"
**Solución:** Asegúrate de tener el entorno virtual activado
```bash
venv\Scripts\activate
```

### Error: "pytest: command not found"
**Solución:** Instala pytest
```bash
pip install pytest pytest-cov
```

### Las pruebas pasan pero no hacen nada
**Solución:** Personaliza los placeholders con tu código real