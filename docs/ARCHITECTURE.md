# Arquitectura del Sistema - Calculadora de Costes IA

Este documento describe la estructura lógica y el flujo de datos de la aplicación. El proyecto sigue un enfoque de **Arquitectura Multicapa** para separar la interfaz de usuario de la lógica aritmética y el consumo de APIs externas.

## 1. Diagrama de Componentes
El sistema se divide en tres capas principales:

* **Capa de Presentación (GUI):** Construida con `CustomTkinter`. Gestiona la entrada del usuario y la visualización de resultados.
* **Capa de Lógica (Core):** El motor de cálculo que procesa los tokens y aplica las tasas de cambio.
* **Capa de Datos/Integración (LiteLLM):** Actúa como fuente de verdad para los precios y modelos actualizados de diversos proveedores (OpenAI, Anthropic, Google).

## 2. Flujo de Datos
1. El usuario introduce texto en la **GUI**.
2. La **GUI** solicita al **Core** (`calculator.py`) una estimación de tokens.
3. El **Core** utiliza `LiteLLM` para obtener el conteo preciso según el modelo seleccionado.
4. Una vez calculado el coste, el **Core** devuelve un diccionario con el desglose (USD, EUR, Cts).
5. La **GUI** formatea y renderiza la información con iconos visuales.

## 3. Decisiones de Diseño
* **Desacoplamiento de Precios:** No almacenamos los precios localmente (excepto en el modo legacy). Delegamos en `LiteLLM` para garantizar que la aplicación no quede obsoleta cuando las APIs bajen sus precios.
* **Inyección de Dependencias:** Los métodos de cálculo reciben el modelo y los tokens como parámetros, permitiendo que la lógica sea testeable sin necesidad de levantar la interfaz gráfica.
* **Robustez (Fallbacks):** Si un modelo no existe en la base de datos de LiteLLM, el sistema aplica una tarifa base para evitar excepciones que cierren la aplicación.