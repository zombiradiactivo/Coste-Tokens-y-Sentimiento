# Sistema de Almacenamiento

## Descripción general

El módulo `almacenamiento/guardar.py` genera dos archivos por cada análisis realizado:

1. **Archivo JSON** — Guarda la estructura completa de datos.
2. **Archivo TXT** — Guarda un resumen legible para el usuario.

## Estructura de directorios de salida

```
resultados/
├── txt/
│   └── analisis_YYYY-MM-DD_HHMMSS.txt
└── json/
    └── analisis_YYYY-MM-DD_HHMMSS.json
```

## Formato JSON

```json
{
    "timestamp": "2026-04-14T12:30:00",
    "texto_analizado": "Me encanta este producto...",
    "niveles": {
        "basico": {"sentimiento": "positivo"},
        "intermedio": {...},
        "avanzado": {...}
    }
}
```

## Formato TXT

```
============================================
ANÁLISIS DE SENTIMIENTO — 2026-04-14 12:30:00
============================================
TEXTO ANALIZADO:
Me encanta este producto. La calidad es excelente...

RESULTADO BÁSICO:     POSITIVO
RESULTADO INTERMEDIO: POSITIVO | polaridad: 0.9 | intensidad: ALTA
JUSTIFICACIÓN:        El texto expresa satisfacción...
```

## Función pública

### `guardar_resultado(datos_totales: dict) -> tuple[str, str]`

- **Input**: Diccionario con `timestamp`, `texto_analizado` y `niveles`.
- **Output**: Tupla con `(ruta_json, ruta_txt)`.
- **Efecto secundario**: Crea directorios `resultados/txt/` y `resultados/json/` si no existen.