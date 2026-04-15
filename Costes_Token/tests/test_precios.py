import pytest
from Costes_Token.core.calculator import CalculadoraCostes

@pytest.fixture
def calc():
    return CalculadoraCostes()

def test_calculo_exacto_conocido(calc):
    """Verifica que el cálculo para 1 millón de tokens en gpt-4o sea correcto."""
    # Nota: gpt-4o suele ser 2.5 in / 10.0 out en la info de litellm
    res = calc.calcular("gpt-4o", 1_000_000, 1_000_000)
    assert res["usd"] == 12.50
    assert res["eur"] == 12.50 * 0.92

def test_estimacion_texto_vacio(calc):
    """Comprueba que un texto vacío no produzca errores y devuelva 0."""
    tokens = calc.estimar_tokens("gpt-4o", "")
    assert tokens == 0

def test_modelo_inexistente_fallback(calc):
    """Verifica que el sistema use precios por defecto si el modelo no existe."""
    res = calc.calcular("non-existent-model", 1000, 1000)
    assert res["usd"] > 0  # Debe aplicar el fallback de 0.00000015 / 0.00000060
    assert isinstance(res["usd"], float)

def test_calculo_tokens_cero(calc):
    """Asegura que con 0 tokens el coste sea 0."""
    res = calc.calcular("gpt-4o", 0, 0)
    assert res["usd"] == 0.0
    assert res["cts"] == 0.0

def test_conversion_moneda(calc):
    """Valida la integridad de la conversión a Euros."""
    res = calc.calcular("gpt-4o", 1_000_000, 0) # 2.50 USD
    expected_eur = 2.50 * 0.92
    assert res["eur"] == pytest.approx(expected_eur)