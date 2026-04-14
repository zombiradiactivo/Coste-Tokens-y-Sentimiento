# Costes Token - Calculadora de Costes de APIs de IA

Herramienta para estimar y calcular los costes de uso de APIs de modelos de lenguaje (LLMs) como GPT-4o, Claude, Gemini, entre otros.

## Descripción

Esta aplicación permite:

- **Seleccionar modelos de IA** de una lista dinámica (más de 100 modelos disponibles via LiteLLM)
- **Estimar tokens** a partir de texto de entrada
- **Calcular costes** en euros, dólares y céntimos
- **Interfaz gráfica** moderna y fácil de usar

## Instalación

1. Clona el repositorio:
```bash
git clone <https://github.com/zombiradiactivo/Coste-Tokens-y-Sentimiento>
cd "Coste Tokens y Sentimiento"
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instala las dependencias:
```bash
pip install tiktoken litellm customtkinter
```

## Uso

Ejecuta la aplicación:
```bash
python Costes_Token/main.py
```

### Pasos:
1. Selecciona un modelo de IA del menú desplegable
2. Introduce el texto a analizar
3. Haz clic en "Calcular Costes"
4. Visualiza los resultados (tokens, euros, dólares, céntimos)

## Estructura de Carpetas

```
Coste Tokens y Sentimiento/
├── Costes_Token/
│   ├── main.py                 # Punto de entrada
│   ├── core/
│   │   ├── __init__.py
│   │   └── calculator.py      # Lógica de cálculo de costes
│   ├── gui/
│   │   ├── __init__.py
│   │   └── app.py             # Interfaz gráfica (CustomTkinter)
│   └── Legacy_Code/
│       └── costesInicio.py   # Código original (referencia)
├── memoriaFinal.md             # Documentación del proyecto
└── README.md                  # Este archivo
```

## Dependencias

- `tiktoken`: Estimación de tokens (OpenAI)
- `litellm`: Precios dinámicos de modelos
- `customtkinter`: Interfaz gráfica moderna

## Licencia

MIT