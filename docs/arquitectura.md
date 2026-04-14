# Arquitectura del Proyecto

## Vista de paquetes

```
Sentimiento/
├── main_litert.py           # Entry point: LiteRT
├── main_ollama.py          # Entry point: Ollama
├── gui_Sentimiento.py     # GUI (tema XP)
├── cliente.py              # Factory de proveedores
├── sentimiento/
│   ├── analizador.py      # Extracción JSON
│   └── niveles.py         # Pipeline 3 niveles
├── almacenamiento/
│   └── guardar.py        # Persistencia
├── Config/
│   └── config.py         # Configuración
├── LiteRT_API/
│   └── LiteRTServerAPI.py
└── Legacy_Code/
    └── InicioSentimiento.py
```

## Flujo de datos

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Input     │ ──► │ Analizador  │ ──► │  Niveles    │ ──► │    GUI      │
│   (Texto)   │     │ (parseo)    │     │  (pipeline) │     │  (display) │ ──► Archivo
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                    │
                                         ┌──────────┴──────────┐
                                         │ Proveedor (API)    │
                                         │ - get_litert_provider()
                                         │ - get_ollama_client()
                                         └────────────────────┘
```

## Pipeline de análisis

| Nivel | Input | Output |
|-------|-------|--------|
| Básico | Texto + prompt | `{"sentimiento": "positivo|negativo|neutral"}` |
| Intermedio | Texto + prompt | `{"sentimiento", "polaridad", "emociones", "intensidad"}` |
| Avanzado | Texto + prompt | `{"sentimiento_global", "polaridad", "fragmentos", "justificacion", "recomendacion"}` |

## Dependencias entre módulos

- `gui_Sentimiento.py` depende de `sentimiento.niveles.analizar` y `almacenamiento.guardar`
- `sentimiento.niveles` depende de `sentimiento.analizador` y `cliente.py`
- `main_litert.py` y `main_ollama.py` dependen de `gui_Sentimiento`, `cliente`, `sentimiento.niveles`