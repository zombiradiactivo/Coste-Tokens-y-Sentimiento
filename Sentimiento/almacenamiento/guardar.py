# almacenamiento/guardar.py
import json
import os
from datetime import datetime

def guardar_resultado(datos_totales: dict):
    """
    Genera dos archivos (TXT y JSON) a partir de los resultados del análisis.
    """
    # 1. Preparar rutas y nombres
    ahora = datetime.now()
    timestamp_file = ahora.strftime("%Y-%m-%d_%H%M%S")
    timestamp_readable = ahora.strftime("%Y-%m-%d %H:%M:%S")
    
    dir_txt = "resultados/txt"
    dir_json = "resultados/json"
    
    for d in [dir_txt, dir_json]:
        os.makedirs(d, exist_ok=True)

    filename_base = f"analisis_{timestamp_file}"

    # --- GENERAR ARCHIVO JSON ---
    path_json = os.path.join(dir_json, f"{filename_base}.json")
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(datos_totales, f, indent=4, ensure_ascii=False)

    # --- GENERAR ARCHIVO TXT ---
    path_txt = os.path.join(dir_txt, f"{filename_base}.txt")
    
    # Extraer datos para el TXT de forma segura
    texto = datos_totales.get("texto_analizado", "N/A")
    res_b = datos_totales.get("niveles", {}).get("basico", {})
    res_i = datos_totales.get("niveles", {}).get("intermedio", {})
    res_a = datos_totales.get("niveles", {}).get("avanzado", {})

    contenido_txt = f"""============================================
ANÁLISIS DE SENTIMIENTO — {timestamp_readable}
============================================
TEXTO ANALIZADO:
{texto}

RESULTADO BÁSICO:     {str(res_b.get('sentimiento', 'N/A')).upper()}
RESULTADO INTERMEDIO: {str(res_i.get('sentimiento', 'N/A')).upper()} | polaridad: {res_i.get('polaridad', 0)} | intensidad: {res_i.get('intensidad', 'N/A')}
JUSTIFICACIÓN:        {res_a.get('justificacion', 'No disponible')}
"""
    
    with open(path_txt, "w", encoding="utf-8") as f:
        f.write(contenido_txt)

    return path_json, path_txt