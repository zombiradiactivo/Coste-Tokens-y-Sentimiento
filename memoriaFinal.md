# Memoria Final del Proyecto

## 1. Contexto del código heredado

**Descripción del problema inicial:**

El código original (`Legacy_Code/costesInicio.py`) era un script monolítico que calculaba costes de uso de APIs de IA. Aunque funcionaba, presentaba varias limitaciones:

- Todo el código concentrado en un único archivo de 126 líneas
- Sin interfaz gráfica, solo salida por consola
- Precios hardcodeados y sin actualización dinámica
- Sin estructura modular, difícil de extender

**Principales deficiencias detectadas:**

- Duplicación de lógica de cálculo en ejemplos consecutivos
- Variables con nombres poco descriptivos en algunos casos
- Sin posibilidad de seleccionar modelos dinámicamente
- Sin integración con herramientas modernas como LiteLLM
- Interfaz de usuario inexistente

---

## 2. Análisis y planificación

**Objetivos de la refactorización:**

- Separar la lógica de negocio de la interfaz gráfica
- Implementar una GUI moderna y funcional
- Integrar LiteLLM para obtener precios dinámicos de modelos
- Mantener compatibilidad con el método original de estimación de tokens
- Crear una estructura modular y extensible

**Plan de trabajo:**

1. Análisis del código original y comprensión del dominio
2. Diseño de arquitectura modular (core/gui)
3. Implementación del núcleo de cálculo con LiteLLM
4. Desarrollo de interfaz gráfica con CustomTkinter
5. Pruebas de funcionalidad y validación de resultados

---

## 3. Modularización del código

**Nueva estructura propuesta:**

```bash
Costes_Token/
├── main.py                  # Punto de entrada
├── core/
│   ├── __init__.py
│   └── calculator.py        # Lógica de negocio
├── gui/
│   ├── __init__.py
│   └── app.py               # Interfaz gráfica
└── Legacy_Code/
    └── costesInicio.py     # Código original
```

**Justificación de la nueva estructura:**

La modularización separa claramente la lógica de negocio (`core/`) de la presentación (`gui/`), lo que permite:
- Mantenibilidad: cambios en la calculadora no afectan la UI
- Extensibilidad: añadir nuevos modelos o funcionalidades sin tocar la interfaz
- Reusabilidad: el núcleo puede usarse en otros proyectos o APIs

**Principales módulos y su función:**

- `main.py`: Punto de entrada que inicializa la aplicación GUI
- `core/calculator.py`: Contains `CalculadoraCostes` and `CalculadoraCostesLocal` for cost calculation logic using LiteLLM and tiktoken
- `gui/app.py`: Interfaz gráfica construida con CustomTkinter con selectors, inputs y visualización de resultados
- `Legacy_Code/costesInicio.py`: Código original conservado como referencia histórica

---

## 4. Implementación del Pipeline

**Descripción del flujo actual:**

```
[Selección de Modelo] → [Entrada de Texto] → [Estimación de Tokens] → [Cálculo de Coste] → [Visualización de Resultados]
```

1. El usuario selecciona un modelo de IA del ComboBox (Lista de LiteLLM)
2. El usuario introduce texto a analizar
3. Al pulsar "Calcular Costes":
   - Se estiman los tokens de entrada usando tiktoken/LiteLLM
   - Se obtiene el precio del modelo desde LiteLLM
   - Se calcula el coste total (input + output)
   - Se muestran resultados en euros, dólares y céntimos

**Gestión de errores y excepciones:**

- Fallback a estimación aproximada (texto/4) si falla tiktoken
- Fallback a precios genéricos si el modelo no está en LiteLLM
- Validación de entrada de texto antes del cálculo

---

## 5. Cambios de código realizados

**Ejemplos de mejoras:**

| Antes | Después | Motivo |
|-------|---------|--------|
| Script monolithico | Módulos core/gui separados | Mejor organización |
| Precios hardcodeados | LiteLLM para precios dinámicos | Actualización automática |
| Sin UI | CustomTkinter GUI | Experiencia de usuario |
| tiktoken único | tiktoken + litellm.token_counter | Mayor compatibilidad |

**Medidas de validación:**

- Ejecución directa del script `python main.py`
- Verificación de resultados contra el código original
- Comparación de costes calculados con precios oficiales

---

## 6. Evaluación final

**Resultados obtenidos:**

- Código modular y mantenible
- Interfaz gráfica funcional y moderna
- Integración con LiteLLM para más de 100 modelos
- Compatible con el código legacy para cálculos básicos
- Estimación de tokens precisa usando encoders especializados

---
