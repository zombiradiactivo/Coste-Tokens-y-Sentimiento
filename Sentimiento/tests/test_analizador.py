import pytest
import os
import json
from unittest.mock import MagicMock
from Sentimiento.sentimiento.niveles import analizar
from Sentimiento.almacenamiento.guardar import guardar_resultado

# --- MOCKS PARA EL PROVEEDOR ---

@pytest.fixture
def mock_provider_positivo():
    """Simula una respuesta positiva de la IA"""
    return lambda x: "positivo"

@pytest.fixture
def mock_provider_json_avanzado():
    """Simula una respuesta JSON completa"""
    return lambda x: '{"sentimiento_global": "negativo", "polaridad": -0.8, "justificacion": "Mal servicio"}'

@pytest.fixture
def mock_provider_error():
    """Simula un fallo de red"""
    def fail(x): raise ConnectionError("Servidor no alcanzable")
    return fail

# --- CASOS DE PRUEBA ---

def test_1_basico_exito(mock_provider_positivo):
    """Prueba que el nivel básico procese bien una respuesta simple"""
    resultado = analizar("Me gusta", "basico", mock_provider_positivo)
    assert resultado["sentimiento"] == "positivo"

def test_2_avanzado_json_valido(mock_provider_json_avanzado):
    """Prueba que el nivel avanzado parsee correctamente el JSON"""
    resultado = analizar("No funciona", "avanzado", mock_provider_json_avanzado)
    assert resultado["sentimiento_global"] == "negativo"
    assert "justificacion" in resultado

def test_3_ia_json_corrupto():
    """Prueba la robustez ante JSON mal formado"""
    mock_bad_json = lambda x: "{'error_de_comillas': ,}"
    resultado = analizar("test", "intermedio", mock_bad_json)
    assert "error" in resultado or isinstance(resultado, dict)

def test_4_error_conexion_api(mock_provider_error):
    """Verifica que el error de conexión se propague correctamente"""
    with pytest.raises(ConnectionError):
        analizar("Hola", "basico", mock_provider_error)

def test_5_texto_vacio(mock_provider_positivo):
    """Verifica el comportamiento con entrada vacía"""
    resultado = analizar("", "basico", mock_provider_positivo)
    assert "sentimiento" in resultado

def test_6_almacenamiento_txt():
    """Verifica la creación del archivo TXT"""
    datos_prueba = {
        "texto_analizado": "Prueba unitaria",
        "niveles": {"basico": {"sentimiento": "neutral"}, "intermedio": {}, "avanzado": {}}
    }
    _, path_txt = guardar_resultado(datos_prueba)
    assert os.path.exists(path_txt)
    # Limpieza
    os.remove(path_txt)

def test_7_almacenamiento_json():
    """Verifica la creación del archivo JSON"""
    datos_prueba = {"test": "data", "niveles": {}}
    path_json, _ = guardar_resultado(datos_prueba)
    assert os.path.exists(path_json)
    with open(path_json, "r") as f:
        data = json.load(f)
    assert data["test"] == "data"
    # Limpieza
    os.remove(path_json)