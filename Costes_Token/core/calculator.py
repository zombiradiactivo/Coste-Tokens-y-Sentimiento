"""
Lógica de negocio para calcular costes de uso de APIs de IA.
"""

import tiktoken
import litellm

class CalculadoraCostesLocal:
    # Precios por millón de tokens según costesInicio.py
    PRECIOS = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "claude-3-sonnet": {"input": 3.00, "output": 15.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }
    
    TASA_CAMBIO_EUR = 0.92  # Ejemplo de tasa USD a EUR

    def __init__(self, modelo="gpt-4o"):
        self.modelo = modelo
        self.precios = self.PRECIOS.get(modelo, self.PRECIOS["gpt-4o-mini"])

    def estimar_tokens(self, texto: str) -> int:
        try:
            encoding = tiktoken.encoding_for_model(self.modelo)
            return len(encoding.encode(texto))
        except Exception as e:
            print(f"ERROR! {e}")
            return len(texto) // 4

    def calcular(self, t_in: int, t_out: int):
        coste_in = (t_in / 1_000_000) * self.precios["input"]
        coste_out = (t_out / 1_000_000) * self.precios["output"]
        total_usd = coste_in + coste_out
        
        return {
            "in": t_in,
            "out": t_out,
            "total_t": t_in + t_out,
            "usd": total_usd,
            "eur": total_usd * self.TASA_CAMBIO_EUR,
            "cts": total_usd * 100
        }
    
class CalculadoraCostes:
    def __init__(self):
        # Lista de modelos comunes para el ComboBox (LiteLLM soporta miles más)
        self.modelos_sugeridos = [
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", 
            "claude-3-5-sonnet-20240620", "gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro"
        ]

    def obtener_lista_modelos(self):
        """Retorna los modelos sugeridos"""
        # return self.modelos_sugeridos
        return litellm.model_list

    def estimar_tokens(self, modelo: str, texto: str) -> int:
        try:
            return litellm.token_counter(model=modelo, text=texto)
        except Exception as e:
            print(f"ERROR! {e}")
            return len(texto) // 4

    def calcular(self, modelo: str, t_in: int, t_out: int):
        try:
            # Obtener info del modelo desde la base de datos de LiteLLM
            info = litellm.get_model_info(modelo)
            # LiteLLM devuelve precios por 1000 tokens habitualmente
            price_in = info.get("input_cost_per_token", 0)
            price_out = info.get("output_cost_per_token", 0) 
        except Exception as e:
            # Fallback a precios genéricos si el modelo no se encuentra
            print(f"ERROR! {e}")
            price_in, price_out = 0.00000015, 0.00000060

        coste_in = t_in * price_in # pyright: ignore[reportOperatorIssue]
        coste_out = t_out * price_out # pyright: ignore[reportOperatorIssue]
        total_usd = coste_in + coste_out
        
        tasa_eur = 0.92 # Tasa de cambio estática 2026

        return {
            "in": t_in,
            "out": t_out,
            "total_t": t_in + t_out,
            "usd": total_usd,
            "eur": total_usd * tasa_eur,
            "cts": total_usd * 100
        }