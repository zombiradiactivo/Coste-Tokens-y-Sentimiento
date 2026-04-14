"""
Ventana principal de la aplicación con la interfaz gráfica.
"""

from core.calculator import CalculadoraCostes
import customtkinter as ctk

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Costes de APIs de IA")
        self.geometry("600x700")
        self.calc = CalculadoraCostes()

        # --- UI: Selección de Modelo ---

        self.frame_selector = ctk.CTkFrame(self, fg_color="#e8e8e8")
        self.frame_selector.pack(pady=10, padx=10, fill="x")

        self.lbl_modelo = ctk.CTkLabel(self.frame_selector, text="Modelo de IA", font=("Comic Sans MS", 14, "bold"), text_color="#2c3e50")
        self.lbl_modelo.pack(pady=(8,0), padx=10, anchor="w")
        
        self.combo_modelo = ctk.CTkComboBox(self.frame_selector, values=self.calc.obtener_lista_modelos(), width=9000)
        self.combo_modelo.set("gpt-4o")
        self.combo_modelo.pack(anchor="w", padx=10, pady=(0,10))

        # --- UI: Texto a analizar ---

        self.frame_text = ctk.CTkFrame(self, fg_color="#e8e8e8")
        self.frame_text.pack(pady=0, padx=10, fill="x")


        self.lbl_texto = ctk.CTkLabel(self.frame_text, text="Texto a analizar", font=("Comic Sans MS", 14, "bold"), text_color="#2c3e50")
        self.lbl_texto.pack(pady=(10, 5), padx=10, anchor="w")
        
        self.txt_input = ctk.CTkTextbox(self.frame_text, height=80, width=9000, corner_radius=10)
        self.txt_input.pack(anchor="w",padx=10, pady=(5,10))

        # --- UI: Botones ---
        self.frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_btns.pack(pady=10, padx=0, fill="x")

        self.btn_calc = ctk.CTkButton(self.frame_btns, height=40, text="Calcular Costes",font=("Comic Sans MS", 14, "bold"), fg_color="#2c3e50", hover_color="#34495e", command=self.ejecutar_calculo)
        self.btn_calc.pack(side="left", padx=5)

        self.btn_clear = ctk.CTkButton(self.frame_btns, height=40, text="Limpiar",font=("Comic Sans MS", 14, "bold"), fg_color="#7f8c8d", hover_color="#95a5a6", command=self.limpiar)
        self.btn_clear.pack(side="left", padx=5)

        self.btn_exit = ctk.CTkButton(self.frame_btns, height=40, text="Salir",font=("Comic Sans MS", 14, "bold"), fg_color="#e74c3c", hover_color="#c0392b", command=self.quit)
        self.btn_exit.pack(side="left", padx=5)

        # --- UI: Resultados (Contenedores con bordes redondeados) ---
        # Sección Tokens

        self.frame_resultados = ctk.CTkFrame(self, fg_color="#e8e8e8", corner_radius=10)
        self.frame_resultados.pack(pady=0, padx=5, fill="x")

        ctk.CTkLabel(self.frame_resultados, text="Resultados", font=("Comic Sans MS", 16, "bold"), text_color="#2c3e50").pack(anchor="w", padx=15, pady=10)

        self.frame_tokens = ctk.CTkFrame(self.frame_resultados, fg_color="#eafaf1", corner_radius=10)
        self.frame_tokens.pack(pady=7, padx=20, fill="x")
        ctk.CTkLabel(self.frame_tokens, text="Tokens", font=("Comic Sans MS", 13, "bold"), text_color="#2c3e50").pack(anchor="w", padx=20, pady=5)
        self.frame_tokens2 = ctk.CTkFrame(self.frame_tokens, fg_color="#ffffff", corner_radius=7)
        self.frame_tokens2.pack(pady=(3,10), padx=10, fill="x")
        self.res_tokens = ctk.CTkLabel(self.frame_tokens2,text="\n\n\n", justify="left", font=("Comic Sans MS", 14))
        self.res_tokens.pack(anchor="nw", padx=(2,5),pady=5 )

        # Sección Costes
        self.frame_costes = ctk.CTkFrame(self.frame_resultados, fg_color="#dae8fc", corner_radius=10)
        self.frame_costes.pack(pady=7, padx=20, fill="x")
        ctk.CTkLabel(self.frame_costes, text="Costes", font=("Comic Sans MS", 13, "bold"), text_color="#2c3e50").pack(anchor="w", padx=20, pady=5)
        self.frame_costes2 = ctk.CTkFrame(self.frame_costes, fg_color="#ffffff", corner_radius=7)
        self.frame_costes2.pack(pady=(3,10), padx=10, fill="x")
        self.res_costes = ctk.CTkLabel(self.frame_costes2, text="\n\n\n", justify="left", font=("Comic Sans MS", 14))
        self.res_costes.pack(anchor="nw", padx=(2,5), pady=5)

    def ejecutar_calculo(self):
        modelo = self.combo_modelo.get()
        texto = self.txt_input.get("1.0", "end-1c")
        
        t_in = self.calc.estimar_tokens(modelo, texto)
        t_out = 200 # Valor de ejemplo solicitado
        res = self.calc.calcular(modelo, t_in, t_out)

        # Actualización de Labels con iconos solicitados
        self.res_tokens.configure(text=(
            f"📥 Entrada: {res['in']} tokens\n"
            f"📤 Salida (estimada): {res['out']} tokens\n"
            f"📊 Total: {res['total_t']} tokens\n"

        ))

        self.res_costes.configure(text=(
            f"💶 Euros: {res['eur']:.6f}€\n"
            f"💵 Dólar: {res['usd']:.6f} $\n"
            f"₵ Céntimos: {res['cts']:.4f} cts\n"
        ))

    def limpiar(self):
        self.txt_input.delete("1.0", "end")
        self.res_tokens.configure(text="")
        self.res_costes.configure(text="")

if __name__ == "__main__":
    app = App()
    app.mainloop()