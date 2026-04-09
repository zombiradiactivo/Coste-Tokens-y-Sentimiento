# ============================================
# ANÁLISIS DE SENTIMIENTO AVANZADO
# ============================================
import os
import json
import re
from typing import Any, Dict, List, Union
from LiteRTServerAPI import enviar_mensaje

#Para buenos resultados usar el modelo Gemma 4 E4B it en LiteRTServerAPI.py

def analizar_sentimiento_basico(texto: str) -> Dict[str, Any]:
    """Nivel básico: solo categoría"""
    
    respuesta = enviar_mensaje("Analiza el sentimiento del texto. Responde SOLO con una palabra: positivo, negativo o neutral."
                                 f"TEXTO: {texto}")

    return {
        "nivel": "básico",
        "sentimiento": respuesta,
        "texto_original": texto[:100] + "..."
    }

def analizar_sentimiento_intermedio(texto: str) -> Dict[str, Any]:
    """Nivel intermedio: polaridad, puntuación, emociones"""
    
    respuesta = enviar_mensaje(
            """
            Analiza el sentimiento del texto. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento: positivo, negativo o neutral
            - polaridad: número entre -1 (muy negativo) y +1 (muy positivo)
            - emociones: objeto con puntuaciones para alegria, tristeza, enojo, sorpresa, miedo
            - intensidad: baja, media, alta
            """
            f"TEXTO: {texto}"
    )
    
    try:
        resultado = json.loads(extraer_json(respuesta))
        resultado["nivel"] = "intermedio"
        resultado["texto_original"] = texto[:100] + "..."
        return resultado
    except:
        return {
            "nivel": "intermedio",
            "error": "No se pudo parsear respuesta",
            "respuesta_raw": respuesta
        }

def analizar_sentimiento_avanzado(texto: str) -> Dict[str, Any]:
    """Nivel avanzado: con justificación y fragmentos relevantes"""
    
    respuesta = enviar_mensaje("""
            Analiza el sentimiento del texto en profundidad. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento_global: positivo, negativo o neutral
            - polaridad: número entre -1 y +1
            - fragmentos: lista de objetos con "texto" y "sentimiento_individual"
            - justificacion: explicación del análisis
            - tonalidad: formal, coloquial, agresivo, entusiasta, etc.
            - recomendacion: qué acción tomar según el sentimiento
            """
            f"TEXTO: {texto}"
    )
    
    try:
        resultado = json.loads(extraer_json(respuesta))
        resultado["nivel"] = "avanzado"
        resultado["texto_original"] = texto[:100] + "..."
        return resultado
    except:
        return {
            "nivel": "avanzado",
            "error": "No se pudo parsear respuesta",
            "respuesta_raw": respuesta
        }

def analizar_sentimiento_multitexto(textos: List[str]) -> Dict[str, Any]:
    """Analiza sentimiento de múltiples textos y calcula estadísticas"""
    
    resultados = []
    for texto in textos:
        resultado = analizar_sentimiento_intermedio(texto)
        resultados.append(resultado)
    
    # Calcular estadísticas agregadas
    polaridades = [r.get("polaridad", 0) for r in resultados if isinstance(r.get("polaridad"), (int, float))]
    
    estadisticas = {
        "total": len(resultados),
        "positivos": sum(1 for r in resultados if r.get("sentimiento") == "positivo"),
        "negativos": sum(1 for r in resultados if r.get("sentimiento") == "negativo"),
        "neutrales": sum(1 for r in resultados if r.get("sentimiento") == "neutral"),
        "polaridad_promedio": sum(polaridades) / len(polaridades) if polaridades else 0
    }
    
    return {
        "resultados_individuales": resultados,
        "estadisticas": estadisticas
    }


def extraer_json(texto: str) -> str:
    # Busca cualquier cosa que esté entre llaves { ... }
    match = re.search(r'(\{.*\})', texto, re.DOTALL)
    return match.group(1) if match else texto

# ========== DEMOSTRACIÓN ==========
print("=" * 70)
print("📊 ANÁLISIS DE SENTIMIENTO - COMPARATIVA DE NIVELES")
print("=" * 70)

texto_prueba = "El producto llegó rápido, pero la calidad no es lo que esperaba. La verdad, estoy un poco decepcionado."

print(f"\n📝 Texto a analizar: {texto_prueba}")
print("-" * 70)

print("\n🔵 NIVEL BÁSICO:")
resultado_basico = analizar_sentimiento_basico(texto_prueba)
print(json.dumps(resultado_basico, indent=2, ensure_ascii=False))

print("\n🔵 NIVEL INTERMEDIO:")
resultado_intermedio = analizar_sentimiento_intermedio(texto_prueba)
print(json.dumps(resultado_intermedio, indent=2, ensure_ascii=False))

print("\n🔵 NIVEL AVANZADO:")
resultado_avanzado = analizar_sentimiento_avanzado(texto_prueba)
print(json.dumps(resultado_avanzado, indent=2, ensure_ascii=False))

# Análisis de múltiples textos (ejemplo de reseñas)
print("\n" + "=" * 70)
print("📊 ANÁLISIS DE MÚLTIPLES RESEÑAS")
print("=" * 70)

reseñas = [
    "Me encantó este producto, súper recomendado",
    "Regular, cumple pero no es nada del otro mundo",
    "Horrible, no compren esto, es una estafa",
    "Buen producto, buen precio, envío rápido",
    "No me gustó, la calidad es mala"
]

# Pylance ahora sabe que resultado_multiple es un Dict[str, Any]
resultado_multiple: Dict[str, Any] = analizar_sentimiento_multitexto(reseñas)

print("\n📈 ESTADÍSTICAS AGREGADAS:")
# Acceso seguro a las claves
stats = resultado_multiple.get('estadisticas', {})
print(f"   Total de reseñas: {stats.get('total')}")
print(f"   Positivas: {stats.get('positivos')}")
print(f"   Negativas: {stats.get('negativos')}")
print(f"   Neutrales: {stats.get('neutrales')}")
print(f"   Polaridad promedio: {stats.get('polaridad_promedio', 0):.2f}")

print("\n📋 RESEÑAS INDIVIDUALES:")
individuales = resultado_multiple.get('resultados_individuales', [])
for i, res in enumerate(individuales):
    print(f"\n   Reseña {i+1}: {reseñas[i]}")
    print(f"   → Sentimiento: {res.get('sentimiento')} (polaridad: {res.get('polaridad', 'N/A')})")
    emociones = res.get('emociones')
    if emociones and isinstance(emociones, dict):
        emocion_principal = max(emociones.items(), key=lambda x: x[1])
        print(f"   → Emoción principal: {emocion_principal[0]}")