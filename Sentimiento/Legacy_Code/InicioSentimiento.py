# ============================================
# ANÁLISIS DE SENTIMIENTO AVANZADO
# ============================================
import os

from dotenv import load_dotenv
import json

from openai import OpenAI ## Faltaba

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analizar_sentimiento_basico(texto: str) -> dict:
    """Nivel básico: solo categoría"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento del texto. Responde SOLO con una palabra: positivo, negativo o neutral.
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    return {
        "nivel": "básico",
        "sentimiento": response.choices[0].message.content.strip(), # type: ignore
        "texto_original": texto[:100] + "..."
    }

def analizar_sentimiento_intermedio(texto: str) -> dict:
    """Nivel intermedio: polaridad, puntuación, emociones"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento del texto. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento: positivo, negativo o neutral
            - polaridad: número entre -1 (muy negativo) y +1 (muy positivo)
            - emociones: objeto con puntuaciones para alegria, tristeza, enojo, sorpresa, miedo
            - intensidad: baja, media, alta
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        resultado = json.loads(response.choices[0].message.content) # type: ignore
        resultado["nivel"] = "intermedio"
        resultado["texto_original"] = texto[:100] + "..."
        return resultado
    except:
        return {
            "nivel": "intermedio",
            "error": "No se pudo parsear respuesta",
            "respuesta_raw": response.choices[0].message.content
        }

def analizar_sentimiento_avanzado(texto: str) -> dict:
    """Nivel avanzado: con justificación y fragmentos relevantes"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento del texto en profundidad. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento_global: positivo, negativo o neutral
            - polaridad: número entre -1 y +1
            - fragmentos: lista de objetos con "texto" y "sentimiento_individual"
            - justificacion: explicación del análisis
            - tonalidad: formal, coloquial, agresivo, entusiasta, etc.
            - recomendacion: qué acción tomar según el sentimiento
            """},
            {"role": "user", "content": texto}
        ],
        temperature=0.0
    )
    
    try:
        resultado = json.loads(response.choices[0].message.content) # type: ignore
        resultado["nivel"] = "avanzado"
        resultado["texto_original"] = texto[:100] + "..."
        return resultado
    except:
        return {
            "nivel": "avanzado",
            "error": "No se pudo parsear respuesta",
            "respuesta_raw": response.choices[0].message.content
        }

def analizar_sentimiento_multitexto(textos: list) -> list:
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
    } # type: ignore

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

resultado_multiple = analizar_sentimiento_multitexto(reseñas)

print("\n📈 ESTADÍSTICAS AGREGADAS:")
print(f"   Total de reseñas: {resultado_multiple['estadisticas']['total']}") # type: ignore
print(f"   Positivas: {resultado_multiple['estadisticas']['positivos']}") # type: ignore
print(f"   Negativas: {resultado_multiple['estadisticas']['negativos']}") # type: ignore
print(f"   Neutrales: {resultado_multiple['estadisticas']['neutrales']}") # type: ignore
print(f"   Polaridad promedio: {resultado_multiple['estadisticas']['polaridad_promedio']:.2f}") # type: ignore

print("\n📋 RESEÑAS INDIVIDUALES:")
for i, res in enumerate(resultado_multiple['resultados_individuales']): # type: ignore
    print(f"\n   Reseña {i+1}: {reseñas[i]}")
    print(f"   → Sentimiento: {res.get('sentimiento')} (polaridad: {res.get('polaridad', 'N/A')})")
    if res.get('emociones'):
        emocion_principal = max(res['emociones'].items(), key=lambda x: x[1]) if res['emociones'] else ("ninguna", 0)
        print(f"   → Emoción principal: {emocion_principal[0]}")