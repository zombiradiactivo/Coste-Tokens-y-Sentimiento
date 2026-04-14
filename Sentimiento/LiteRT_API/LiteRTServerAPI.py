import requests

def enviar_mensaje(mensaje, model_id="gemma-4-E4B-it"):
    # LiteRT Server Android [https://github.com/zombiradiactivo/LiteRT-Server-Android]
    # Configurar la url a la ip del dispositivo ejecutando la aplicacion 
    # Configurar el model_id al modelo en ejecucion del dispositivo

    url = "http://10.46.191.232:8080/api/chat"
    
    # Definimos los datos siguiendo el formato 'form-data' que usa la web / Actualmente no se puede configurar el system prompt
    payload = {
        'message': mensaje,
        'model_id': model_id
    }

    try:
        # Realizamos la petición POST con timeout de 120 segundos
        response = requests.post(url, data=payload, timeout=120)
        
        # Verificamos si la respuesta fue exitosa (código 200)
        response.raise_for_status()
        
        # Parseamos el JSON de respuesta
        data = response.json()
        
        if data.get("success"):
            return data.get("message")
        else:
            return "Error: La API respondió pero no fue exitoso."
            
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"

# --- Ejemplo de uso interactivo ---
# if __name__ == "__main__":
#     respuesta = enviar_mensaje("Analiza el sentimiento del texto. Responde SOLO con una palabra: positivo, negativo o neutral. TEXTO: El producto llegó rápido, pero la calidad no es lo que esperaba. La verdad, estoy un poco decepcionado.")
#     print(f"{respuesta}\n")
#     respuesta2 = enviar_mensaje("""
#             Analiza el sentimiento del texto en profundidad. Responde ÚNICAMENTE en formato JSON con:
#             - sentimiento_global: positivo, negativo o neutral
#             - polaridad: número entre -1 y +1
#             - fragmentos: lista de objetos con "texto" y "sentimiento_individual"
#             - justificacion: explicación del análisis
#             - tonalidad: formal, coloquial, agresivo, entusiasta, etc.
#             - recomendacion: qué acción tomar según el sentimiento
#             """ 
#             "El producto llegó rápido, pero la calidad no es lo que esperaba. La verdad, estoy un poco decepcionado."
#         )
#     print(f"{respuesta2}\n")
