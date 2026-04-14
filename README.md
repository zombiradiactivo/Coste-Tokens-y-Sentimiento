# Análisis de Sentimiento

**Estado del pipeline:** ![CI](https://github.com/anomalyco/opencode/actions/workflows/ci.yml/badge.svg)

Sistema de análisis de sentimiento en 3 niveles mediante modelos LLM locales (LiteRT u Ollama).

## Descripción

Proyecto de análisis de texto que evalúa el sentimiento en tres niveles de profundidad:
- **Básico**: Clasificación Simple (positivo/negativo/neutral)
- **Intermedio**: Polaridad, emociones e intensidad
- **Avanzado**: Fragmentos, justificación y recomendaciones

Soporta múltiples proveedores de IA:
- **LiteRT** (servidor externo)
- **Ollama** (modelo local qwen3.5:0.8b)

## Instalación

```bash
# Clonar el repositorio
git clone <https://github.com/zombiradiactivo/Coste-Tokens-y-Sentimiento>
cd Sentimiento

# Instalar dependencias
pip install openai requests pytest
```

## Uso

### Desde línea de comandos

```bash
# Ejecutar con LiteRT
python main_litert.py

# Ejecutar con Ollama
python main_ollama.py
```

### Desde Python

```python
from sentimiento.niveles import analizar
from cliente import get_litert_provider

provider = get_litert_provider()
resultado = analizar("Me encanta este producto", "basico", provider)
print(resultado)
```

## Estructura de carpetas

```
Sentimiento/
├── main_litert.py              # Entry point LiteRT
├── main_ollama.py             # Entry point Ollama
├── gui_Sentimiento.py        # Interfaz GUI (tema XP)
├── cliente.py                # Factory de proveedores
├── docs/                     # Documentación
│   ├── arquitectura.md
│   ├── almacenamiento.md
│   └── api_referencia.md
├── sentimiento/
│   ├── analizador.py         # Extracción JSON
│   └── niveles.py            # Pipeline de análisis
├── almacenamiento/
│   └── guardar.py            # Persistencia
├── Config/
│   └── config.py             # Configuración
├── LiteRT_API/
│   └── LiteRTServerAPI.py    # API LiteRT
├── tests/
│   └── test_analizador.py    # Tests unitarios
├── resultados/              # Resultados generados
│   ├── txt/                # Archivos .txt
│   └── json/               # Archivos .json
└── Legacy_Code/
    └── InicioSentimiento.py # Código original
```

## Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar un test específico
pytest tests/test_analizador.py -v
```

## Configuración

Editar `Config/config.py` para ajustar:
- `OLLAMA_SERVER_IP` — URL del servidor Ollama
- `LITERT_SERVER_IP` — URL del servidor LiteRT
- `OLLAMA_MODEL_NAME` — Modelo a usar

## Resultados

Los análisis se guardan automáticamente en:
- `resultados/json/analisis_YYYY-MM-DD_HHMMSS.json`
- `resultados/txt/analisis_YYYY-MM-DD_HHMMSS.txt`