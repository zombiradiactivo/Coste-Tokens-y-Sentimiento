import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AnalisisSentimientoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Sentimiento - Local")
        
        # Intentar establecer el icono nativo de Windows (hoja)
        try:
            # Esto funciona en Windows si hay un icono de sistema por defecto.
            # No es esencial para la funcionalidad.
            self.root.iconbitmap(default='') 
        except Exception:
            pass

        # Configuración de estilo global
        style = ttk.Style()
        style.theme_use('vista') # Usar el tema de vista/windows nativo
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TLabel', background='#F0F0F0', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9))
        style.configure('TCheckbutton', background='#F0F0F0', font=('Segoe UI', 9))
        
        # Configuración específica para el título principal
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), background='#F0F0F0')

        # Contenedor principal con padding
        main_container = ttk.Frame(root, padding="15 15 15 10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN 1: TÍTULO PRINCIPAL ---
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 15))
        
        # Icono de la carpeta/libro (usando caracteres unicode similares)
        # Nota: Un icono real requeriría un archivo de imagen. Usamos un unicode aproximado.
        lbl_icon = ttk.Label(header_frame, text="🗁", font=('Segoe UI', 14))
        lbl_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        lbl_title = ttk.Label(header_frame, text="ANÁLISIS DE SENTIMIENTO - LOCAL", style='Header.TLabel')
        lbl_title.pack(side=tk.LEFT)

        # --- SECCIÓN 2: TEXTO A ANALIZAR ---
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.BOTH, pady=(0, 15))

        lbl_input = ttk.Label(input_frame, text="📝 Texto a analizar")
        lbl_input.pack(anchor=tk.W, pady=(0, 5))

        # Cuadro de texto con scrollbar
        text_scroll = ttk.Scrollbar(input_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_input = tk.Text(input_frame, height=4, font=('Segoe UI', 9), wrap=tk.WORD, 
                                 bd=1, relief=tk.SOLID, yscrollcommand=text_scroll.set)
        self.txt_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=self.txt_input.yview)

        # Insertar el texto de ejemplo de la imagen
        texto_ejemplo = "Me encanta este producto. La calidad es excelente y el servicio al cliente es maravilloso. Definitivamente lo recomendaría a mis amigos."
        self.txt_input.insert(tk.END, texto_ejemplo)

        # --- SECCIÓN 3: BOTONES DE ACCIÓN ---
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 15))

        # Estilo para botones con iconos
        style.configure('ActionButton.TButton', padding="5 2")

        self.btn_analizar = ttk.Button(button_frame, text="🔍 ANALIZAR SENTIMIENTO", 
                                         style='ActionButton.TButton', command=self.simular_analisis)
        self.btn_analizar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_limpiar = ttk.Button(button_frame, text="🧹 LIMPIAR", 
                                        style='ActionButton.TButton', command=self.limpiar_texto)
        self.btn_limpiar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_guardar = ttk.Button(button_frame, text="💾 GUARDAR", 
                                        style='ActionButton.TButton', command=self.guardar_resultado)
        self.btn_guardar.pack(side=tk.LEFT)

        # --- SECCIÓN 4: PANELES DE PESTAÑAS (Notebook) ---
        notebook_frame = ttk.Frame(main_container)
        notebook_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Resultados por Nivel
        tab_resultados = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(tab_resultados, text="📊 Resultados por Nivel")

        # Configurar la tabla (Treeview)
        columns = ("nivel", "sentimiento", "polaridad", "intensidad")
        self.tree = ttk.Treeview(tab_resultados, columns=columns, show="headings", height=8)
        
        # Definir encabezados de columna
        self.tree.heading("nivel", text="Nivel", anchor=tk.CENTER)
        self.tree.heading("sentimiento", text="Sentimiento", anchor=tk.CENTER)
        self.tree.heading("polaridad", text="Polaridad", anchor=tk.CENTER)
        self.tree.heading("intensidad", text="Intensidad", anchor=tk.CENTER)

        # Definir anchos de columna y alineación
        self.tree.column("nivel", width=150, anchor=tk.CENTER)
        self.tree.column("sentimiento", width=180, anchor=tk.CENTER)
        self.tree.column("polaridad", width=180, anchor=tk.CENTER)
        self.tree.column("intensidad", width=150, anchor=tk.CENTER)

        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(tab_resultados, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar tags para el color de fondo (filas verdes)
        self.tree.tag_configure('favorable', background='#E6F4EA') # Verde muy claro

        # Insertar los datos de ejemplo de la imagen
        self.insertar_datos_ejemplo()

        # Otras pestañas (vacías para fidelidad visual)
        tab_detallado = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(tab_detallado, text="📖 Análisis Detallado")
        ttk.Label(tab_detallado, text="(Contenido de análisis detallado vaya aquí)").pack()

        tab_justificacion = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(tab_justificacion, text="💡 Justificación & Recomendación")
        ttk.Label(tab_justificacion, text="(Justificación vaya aquí)").pack()

        tab_historial = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(tab_historial, text="📅 Historial")
        ttk.Label(tab_historial, text="(Lista de historial vaya aquí)").pack()

        # --- SECCIÓN 5: LEYENDA DE POLARIDAD ---
        legend_frame = ttk.LabelFrame(main_container, text="❓ ¿Qué significa la polaridad?", padding="10 10")
        legend_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 10))

        # Usar Text widget para formatear colores fácilmente en lugar de Labels múltiples
        legend_text = tk.Text(legend_frame, font=('Segoe UI', 9), height=3, bg='#F0F0F0', wrap=tk.WORD, bd=0)
        legend_text.pack(fill=tk.X)
        
        # Configurar tags de color
        legend_text.tag_config("verde", foreground="#228B22") # ForestGreen
        legend_text.tag_config("rojo", foreground="#DC143C")  # Crimson
        legend_text.tag_config("gris", foreground="#808080")  # Gray

        # Insertar texto con formato
        legend_text.insert(tk.END, "● POSITIVA", "verde")
        legend_text.insert(tk.END, " (+0.00 a +1.00): El texto expresa emociones positivas\n")
        
        legend_text.insert(tk.END, "● NEGATIVA", "rojo")
        legend_text.insert(tk.END, " (-1.00 a -0.00): El texto expresa emociones negativas\n")
        
        legend_text.insert(tk.END, "○ NEUTRAL", "gris")
        legend_text.insert(tk.END, " (0.00): El texto no muestra emociones fuertes")

        legend_text.config(state=tk.DISABLED) # Hacerlo de solo lectura

        # --- SECCIÓN 6: BARRA DE ESTADO INFERIOR ---
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, anchor=tk.W, pady=(5, 0))

        self.check_auto_save_var = tk.BooleanVar(value=True)
        self.check_auto_save = ttk.Checkbutton(status_frame, text="Análisis completado y guardado automáticamente", 
                                                variable=self.check_auto_save_var)
        self.check_auto_save.pack(side=tk.LEFT)

    def insertar_datos_ejemplo(self):
        # Datos de la imagen: Nivel, Sentimiento, Polaridad, Intensidad
        data = [
            ("● Básico", "POSITIVO", "90.99%", "-"),
            ("○ Intermedio", "POSITIVO", "0.9", "ALTA"),
            ("● Avanzado", "POSITIVO", "0.9", "-")
        ]
        
        for item in data:
            # Aplicar tag 'favorable' a todas las filas para el fondo verde
            self.tree.insert("", tk.END, values=item, tags=('favorable',))

    def simular_analisis(self):
        # Función dummy para el botón
        texto = self.txt_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Atención", "Por favor, introduce texto para analizar.")
            return
        
        # En una app real, aquí iría la lógica de IA.
        messagebox.showinfo("Simulación", f"Iniciando análisis simulado para:\n'{texto[:30]}...'")
        
    def limpiar_texto(self):
        self.txt_input.delete("1.0", tk.END)
        # Limpiar también la tabla si se desea
        for item in self.tree.get_children():
            self.tree.delete(item)

    def guardar_resultado(self):
        messagebox.showinfo("Guardar", "Resultado guardado (simulación).")

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    
    # Establecer dimensiones iniciales
    root.geometry("850x700")
    
    # Iniciar la aplicación
    app = AnalisisSentimientoGUI(root)
    root.mainloop()