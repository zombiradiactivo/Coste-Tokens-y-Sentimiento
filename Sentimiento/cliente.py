# sentimiento/cliente.py
import os
from openai import OpenAI
from Config.config import OLLAMA_SERVER_IP, OLLAMA_MODEL_NAME

def get_ollama_client():
    return OpenAI(base_url=OLLAMA_SERVER_IP, api_key='ollama')

def get_litert_provider():
    # Retorna la referencia a la función de envío de LiteRT
    from LiteRT_API.LiteRTServerAPI import enviar_mensaje
    return enviar_mensaje