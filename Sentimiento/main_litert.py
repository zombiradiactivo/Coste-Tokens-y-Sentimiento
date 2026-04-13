# main_litert.py
import tkinter as tk
from gui_Sentimiento import AnalisisSentimientoGUI_XP
from cliente import get_litert_provider
from sentimiento.niveles import analizar

def proveedor_litert(prompt):
    func = get_litert_provider()
    return func(prompt)

if __name__ == "__main__":
    root = tk.Tk()
    # Inyectamos la función de LiteRT en la GUI
    app = AnalisisSentimientoGUI_XP(root, engine_func=analizar, provider=proveedor_litert)
    root.mainloop()