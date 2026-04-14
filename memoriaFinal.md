# 🧠 Memoria Final del Proyecto

## 1. Contexto del código heredado
**Descripción del problema inicial:**
El proyecto iniciaba como un script monolítico (`Legacy_Code/InicioSentimiento.py`) que incluía todo el flujo: entrada de texto, llamada a la API, procesamiento de resultados y guardado en un único archivo sin estructura modular.

**Principales deficiencias detectadas:**
- Todo el código concentrado en un único archivo (`InicioSentimiento.py`).
- Sin separación entre capa de presentación, lógica de negocio y persistencia.
- Variables con nombres genéricos y falta de tipado.
- Repetición de lógica de parsing y formateo en múltiples lugares.
- Acoplamiento directo a una única API (sin abstracción de proveedores).

**Captura o esquema del flujo original:**
```python
# Pseudocódigo del código original
texto = input("Escribe el texto: ")
respuesta = requests.post(url, data={"prompt": texto})
print(respuesta.json())
# Sin validación, sin gestión de errores, sin guardar estructurado
```

---

## 2. Análisis y planificación
**Objetivos de la refactorización:**
- Separar responsabilidades en módulos independientes.
- Implementar un pipeline de análisis por niveles (básico, intermedio, avanzado).
- Abstraer el proveedor de IA para soportar múltiples backends (LiteRT, Ollama).
- Crear una GUI desacoplada con tema Windows XP.

**Plan de trabajo:**
- Fase 1: Crear módulos core (`sentimiento/`, `almacenamiento/`, `Config/`, `cliente.py`).
- Fase 2: Implementar pipeline de análisis de 3 niveles.
- Fase 3: Desarrollar GUI con tkinter y tema XP.
- Fase 4: Abstraer proveedores de API (LiteRT, Ollama).
- Fase 5: Pruebas funcionales del pipeline completo.

---

## 3. Modularización del código
**Nueva estructura:**
```bash
Sentimiento/
├── main_litert.py           # Entry point LiteRT
├── main_ollama.py          # Entry point Ollama
├── gui_Sentimiento.py     # Interfaz GUI (tema XP)
├── cliente.py             # Abstracción de proveedores
├── sentimiento/
│   ├── analizador.py    # Extracción y formateo JSON
│   └── niveles.py      # Pipeline de análisis (3 niveles)
├── almacenamiento/
│   └── guardar.py     # Persistencia (JSON + TXT)
├── Config/
│   └── config.py       # Configuración centralizada
├── LiteRT_API/
│   └── LiteRTServerAPI.py  # Implementación LiteRT
└── Legacy_Code/
    └── InicioSentimiento.py  # Código original (referencia)
```

**Justificación de la nueva estructura:**
La separación en módulos permite escalar el proyecto sin modificar código existente. Cada módulo tiene una responsabilidad única: el módulo `sentimiento` maneja la lógica de análisis, `almacenamiento` gestiona la persistencia, `cliente` abstrae el proveedor de IA, y `gui` mantiene la presentación independiente de la lógica de negocio.

**Principales módulos y su función:**
- `sentimiento/analizador.py`: Extrae JSON de respuestas y estandariza el formato de salida.
- `sentimiento/niveles.py`: Implementa el pipeline de 3 niveles (básico → intermedio → avanzado).
- `almacenamiento/guardar.py`: Genera archivos JSON y TXT con timestamps.
- `cliente.py`: Factory que retorna el proveedor de API seleccionado (`get_litert_provider`, `get_ollama_client`).
- `Config/config.py`: Centraliza IPs de servidores y nombres de modelos.

---

## 4. Implementación del Pipeline
**Descripción del flujo actual:**
```
[Texto Input]
    │
    ▼
┌─────────────────────┐
│   Nivel Básico     │ ──► Sentimiento simple (positivo/negativo/neutral)
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Nivel Intermedio   │ ──► JSON: sentimiento, polaridad, emociones, intensidad
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Nivel Avanzado     │ ──► JSON: sentimiento_global, polaridad, fragmentos, justificación, recomendación
└─────────────────────┘
    │
    ▼
[GUI / Archivos salida]
```

**Diagrama del pipeline:**
```text
[Entrada Texto] → [analizador.extraer_json] → [niveles.analizar] → [gui_Sentimiento] → [almacenamiento.guardar]
```

**Gestión de errores y excepciones:**
- Try/except en cada nivel para capturar errores de parseo JSON.
- Fallback en `niveles.py` que retorna `{"error": "Error de parseo", "raw": ...}` cuando el modelo no responde en formato válido.
- Mensajes de error en la GUI mediante `messagebox.showerror`.
- Logging implícito mediante los archivos TXT generados con el resultado.

---

## 5. Cambios de código realizados
**Ejemplos de mejoras:**
| Antes | Después | Motivo |
|-------|----------|--------|
| `requests.post(url, json={"prompt": texto})` | `enviar_mensaje(prompt)` (abstraído en `cliente.py`) | Desacoplamiento del provider |
| Todo en un archivo | Módulos independientes (`sentimiento/`, `almacenamiento/`, `Config/`) | Mantenibilidad y escalabilidad |
| Sin validación JSON | `try/except json.loads()` en `niveles.py` | Robustez ante respuestas inválidas |
| Sin guardar estructurado | `almacenamiento.guardar.py` genera TXT y JSON | Trazabilidad de resultados |
| GUI mezclada con lógica | `gui_Sentimiento.py` recibe funciones como parámetros | Dependecy injection |

**Medidas de validación:**
- Pruebas manuales con la GUI mediante texto de ejemplo precargado.
- Comparación de salida JSON entre niveles.
- Generación correcta de archivos en `resultados/txt/` y `resultados/json/`.
- Verificación de conexión a servidores LiteRT/Ollama.

---

## 6. Evaluación final
**Resultados obtenidos:**
- ✅ El código ahora está separado en módulos independientes con responsabilidades claras.
- ✅ El pipeline de 3 niveles funciona correctamente con ambos proveedores (LiteRT y Ollama).
- ✅ La GUI está desacoplada y themed con estilo Windows XP.
- ✅ Los resultados se guardan automáticamente en JSON y TXT con timestamps.
- ✅ El proyecto es extensible: añadir un nuevo provider solo requiere crear una función en `cliente.py`.
