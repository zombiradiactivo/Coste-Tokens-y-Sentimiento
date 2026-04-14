# Referencia de API

## Módulo: sentimiento.analizador

### `extraer_json(texto: str) -> str`

Extrae el primer bloque JSON de una respuesta de texto libre.

- **Parámetros**:
  - `texto` (str): Respuesta sin formato del modelo.
- **Retorna**: String con el JSON extraído o el texto original si no se encuentra.

### `formatear_resultado(nivel: str, texto: str, respuesta: Any) -> dict`

Estandariza el formato de salida por nivel.

- **Parámetros**:
  - `nivel` (str): Nivel del análisis ("basico", "intermedio", "avanzado").
  - `texto` (str): Texto original analizado.
  - `respuesta` (Any): Respuesta cruda del proveedor.
- **Retorna**: Dictionary con `nivel`, `texto_original` y `data`.

---

## Módulo: sentimiento.niveles

### `analizar(texto: str, nivel: str, provider_func) -> dict`

Ejecuta el análisis de sentimiento para un nivel específico.

- **Parámetros**:
  - `texto` (str): Texto a analizar.
  - `nivel` (str): Nivel de análisis ("basico", "intermedio", "avanzado").
  - `provider_func` (callable): Función proveedora (e.g., `enviar_mensaje`).
- **Retorna**: Dictionary con el resultado del análisis.

---

## Módulo: almacenamiento.guardar

### `guardar_resultado(datos_totales: dict) -> tuple[str, str]`

Genera archivos JSON y TXT con los resultados.

- **Parámetros**:
  - `datos_totales` (dict): Diccionario con `timestamp`, `texto_analizado`, `niveles`.
- **Retorna**: Tupla `(ruta_json, ruta_txt)`.
- **Efecto secundario**: Crea directorios `resultados/txt/` y `resultados/json/` si no existen.

---

## Módulo: cliente

### `get_ollama_client() -> OpenAI`

Retorna cliente de OpenAI configurado para Ollama.

- **Retorna**: Instancia de `OpenAI` con base_url configurada.

### `get_litert_provider() -> callable`

Retorna la función `enviar_mensaje` de LiteRT.

- **Retorna**: Función `callable` para enviar prompts al servidor LiteRT.

---

## Módulo: Config.config

Constantes de configuración del proyecto.

- `OLLAMA_SERVER_IP` (str): URL del servidor Ollama.
- `LITERT_SERVER_IP` (str): URL del servidor LiteRT.
- `OLLAMA_MODEL_NAME` (str): Nombre del modelo Ollama a usar.

---

## Módulo: gui_Sentimiento

### Clase: `AnalisisSentimientoGUI_XP`

Interfaz gráfica con tema Windows XP.

#### Constructor

```python
def __init__(self, root, engine_func, provider)
```

- **Parámetros**:
  - `root` (tk.Tk): Ventana raíz de tkinter.
  - `engine_func` (callable): Función `analizar` de `sentimiento.niveles`.
  - `provider` (callable): Proveedor de IA (`get_litert_provider()` o similar).

#### Métodos públicos

- `lanzar_analisis()`: Inicia el análisis de texto desde la GUI.
- `limpiar()`: Limpia todos los campos de entrada y resultados.
- `ejecutar_guardado()`: Guarda el último resultado en archivos.