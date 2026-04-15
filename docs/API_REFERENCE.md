# Referencia de la API - Módulo Core

Documentación técnica de las clases y métodos disponibles en `core/calculator.py`.

## Clase: `CalculadoraCostes`

Es la clase principal encargada de la comunicación con las librerías de conteo y la gestión de la lógica de negocio.

### Métodos

#### `obtener_lista_modelos(self) -> list`
Retorna una lista de strings con los identificadores de modelos soportados por la librería base.
* **Retorno:** `list` de nombres de modelos (ej. `gpt-4o`, `claude-3-5-sonnet`).

#### `estimar_tokens(self, modelo: str, texto: str) -> int`
Calcula la cantidad de tokens que representa un texto para un modelo específico.
* **Parámetros:**
    * `modelo` (str): Identificador del modelo (ej. "gpt-4o").
    * `texto` (str): El contenido a analizar.
* **Retorno:** `int` (Número de tokens).
* **Nota:** Si el modelo no es compatible, realiza una estimación por defecto (caracteres / 4).

#### `calcular(self, modelo: str, t_in: int, t_out: int) -> dict`
Realiza el cálculo financiero basado en el uso de tokens.
* **Parámetros:**
    * `modelo` (str): Nombre del modelo para buscar su tarifa.
    * `t_in` (int): Tokens de entrada (prompt).
    * `t_out` (int): Tokens de salida (completación).
* **Retorno:** `dict` con la siguiente estructura:
    ```json
    {
        "in": int,       // Tokens de entrada
        "out": int,      // Tokens de salida
        "total_t": int,  // Suma total de tokens
        "usd": float,    // Coste total en Dólares
        "eur": float,    // Coste total en Euros (Tasa 0.92)
        "cts": float     // Coste total en Céntimos de Dólar
    }
    ```

---

## Clase: `CalculadoraCostesLocal` (Legacy)
*Uso interno para entornos sin conexión o modelos predefinidos.*

### Atributos
* `PRECIOS`: Diccionario estático con tarifas de modelos comunes.
* `TASA_CAMBIO_EUR`: Constante fijada en `0.92`.