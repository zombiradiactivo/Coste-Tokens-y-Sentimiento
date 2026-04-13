# sentimiento/niveles.py
from .analizador import extraer_json, formatear_resultado
import json

def analizar(texto: str, nivel: str, provider_func) -> dict:
    prompts = {
        "basico": f"Analiza el sentimiento. Responde SOLO: positivo, negativo o neutral. TEXTO: {texto}",
        "intermedio": f"Analiza el sentimiento. Responde ÚNICAMENTE JSON: {{sentimiento, polaridad (-1 a 1), emociones, intensidad}}. TEXTO: {texto}",
        "avanzado": f"Analiza profundidad. Responde ÚNICAMENTE JSON: {{sentimiento_global, polaridad, fragmentos, justificacion, recomendacion}}. TEXTO: {texto}"
    }
    
    # Aquí provider_func puede ser enviar_mensaje (LiteRT) o una función que use OpenAI (Ollama)
    raw_res = provider_func(prompts[nivel])
    
    if nivel == "basico":
        return {"sentimiento": raw_res.strip().lower()}
    
    try:
        return json.loads(extraer_json(raw_res))
    except:
        return {"error": "Error de parseo", "raw": raw_res}