# main_ollama.py
import tkinter as tk
from gui_Sentimiento import AnalisisSentimientoGUI_XP
from cliente import get_ollama_client
from Config.config import OLLAMA_MODEL_NAME
from sentimiento.niveles import analizar

client = get_ollama_client()

def proveedor_ollama(prompt):
    res = client.chat.completions.create(
        model=OLLAMA_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        reasoning_effort="none"
    )
    return res.choices[0].message.content

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisisSentimientoGUI_XP(root, engine_func=analizar, provider=proveedor_ollama)
    root.mainloop()