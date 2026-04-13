# sentimiento/analizador.py
import json
import re
from typing import Dict, Any

def extraer_json(texto: str) -> str:
    match = re.search(r'(\{.*\})', texto, re.DOTALL)
    return match.group(1) if match else texto

def formatear_resultado(nivel: str, texto: str, respuesta: Any) -> Dict[str, Any]:
    """Estandariza la salida de todos los niveles."""
    return {
        "nivel": nivel,
        "texto_original": texto[:100] + "...",
        "data": respuesta
    }