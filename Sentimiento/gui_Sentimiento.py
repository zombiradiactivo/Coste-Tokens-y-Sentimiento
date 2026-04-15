import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
import os
import glob
from datetime import datetime
from almacenamiento.guardar import guardar_resultado



class AnalisisSentimientoGUI_XP:
    def __init__(self, root, engine_func, provider):
        self.root = root
        self.root.title("Análisis de Sentimiento - Local")
        
        self.root.geometry("800x700")
        self.root.minsize(770, 600)

        self.analizar_fn = engine_func  # La función 'analizar' de niveles.py
        self.provider = provider        # El proveedor (LiteRT u Ollama)

        # 1. FORZAR TEMA CLÁSICO Y COLORES DE WINDOWS XP
        self.root.tk.call('tk', 'useinput', '1')
        self.root.configure(background='#dcdad5') # Gris clásico de XP
        
        # Guardar los últimos resultados para poder exportarlos
        self.ultimo_resultado = {}

        style = ttk.Style()
        style.theme_use('winnative') # Usar el motor clásico de Windows

        # 2. DEFINIR COLORES Y ESTILOS ESPECÍFICOS XP
        # Color de fondo de ventana (gris)
        bg_color = '#dcdad5'
        # Color de fondo de widgets (blanco, como los cuadros de texto)
        white_bg = 'white'
        # Fuentes (Segoe UI es demasiado moderna para XP puro, pero se ve mejor en pantallas nuevas)
        font_base = ('Tahoma', 8) # Tahoma es más fiel a XP
        font_bold = ('Tahoma', 8, 'bold')
        font_title = ('Arial', 10, 'bold')

        # Configuración general de estilos de widgets
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, font=font_base, foreground='black')
        
        # Estilo para botones con relieve XP
        style.configure('TButton', font=font_base, padding=2)
        style.map('TButton',
                  foreground=[('disabled', '#808080')],
                  background=[('active', '#DEDBD5')])

        # Estilo para las pestañas (Notebooks) de XP
        style.configure('TNotebook', background=bg_color, tabposition='nw', borderwidth=1)
        style.configure('TNotebook.Tab', font=font_base, padding=(4, 2), background='#E1DED8')
        style.map('TNotebook.Tab',
                  background=[('selected', bg_color), ('active', '#D6D3CD')],
                  expand=[('selected', [0, 0, 0, 1])]) # Simular relieve

        # Estilo para los cuadros de etiquetas con borde (Labelframe)
        style.configure('TLabelframe', background=bg_color, borderwidth=2, relief='groove')
        style.configure('TLabelframe.Label', background=bg_color, font=font_bold, foreground='black')

        # Estilo para la tabla (Treeview)
        style.configure('Treeview', font=font_base, rowheight=20, borderwidth=1, relief='sunken')
        style.configure('Treeview.Heading', font=font_bold, background=bg_color)
        
        # Estilo Checkbutton
        style.configure('TCheckbutton', background=bg_color, font=font_base)

        # Contenedor principal
        main_container = ttk.Frame(root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN 1: TÍTULO PRINCIPAL ---
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 10))
        
        # Icono de la carpeta (carácter unicode para mayor facilidad)
        lbl_icon = ttk.Label(header_frame, text="🗁", font=('Segoe UI', 12), foreground='black')
        lbl_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        lbl_title = ttk.Label(header_frame, text="ANÁLISIS DE SENTIMIENTO - LOCAL", font=font_title, background=bg_color, foreground='black')
        lbl_title.pack(side=tk.LEFT)

        # --- SECCIÓN 2: TEXTO A ANALIZAR ---
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.BOTH, pady=(0, 10))

        lbl_input = ttk.Label(input_frame, text="📝 Texto a analizar")
        lbl_input.pack(anchor=tk.W, pady=(0, 2))

        # Marco con relieve hundido para el Text widget
        text_border_frame = tk.Frame(input_frame, relief='sunken', borderwidth=2, bg=white_bg)
        text_border_frame.pack(fill=tk.BOTH, expand=True)

        text_scroll = ttk.Scrollbar(text_border_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_input = tk.Text(text_border_frame, height=4, font=('Segoe UI', 9), wrap=tk.WORD, 
                                 bd=0, bg=white_bg, yscrollcommand=text_scroll.set, foreground='black', 
                                 insertbackground='black')
        self.txt_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=self.txt_input.yview)

        # Texto de ejemplo
        texto_ejemplo = "Me encanta este producto. La calidad es excelente y el servicio al cliente es maravilloso. Definitivamente lo recomendaría a mis amigos."
        self.txt_input.insert(tk.END, texto_ejemplo)

        # --- SECCIÓN 3: BOTONES DE ACCIÓN ---
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 10))

        self.btn_analizar = ttk.Button(button_frame, text="🔍 ANALIZAR SENTIMIENTO", style='TButton', command=self.lanzar_analisis)
        self.btn_analizar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = ttk.Button(button_frame, text="🧹 LIMPIAR", style='TButton', command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_guardar = ttk.Button(button_frame, text="💾 GUARDAR", style='TButton', command=self.ejecutar_guardado)
        self.btn_guardar.pack(side=tk.LEFT)

        # --- SECCIÓN 4: PANELES DE PESTAÑAS (Notebook) ---
        self.notebook = ttk.Notebook(main_container, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Tab 1: Tabla
        self.tab_tabla = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.tab_tabla, text="📊 Resultados por Nivel")
        
        cols = ("nivel", "sentimiento", "polaridad", "intensidad")
        self.tree = ttk.Treeview(self.tab_tabla, columns=cols, show="headings", height=6)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.tag_configure('favorable', background='#ECFBF0') # Verde XP
        self.tree.tag_configure('desfavorable', background='#FCE8E6') # Rojo suave

        # Tab 2: Detalle JSON
        self.tab_json = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_json, text="📖 Análisis Detallado")
        self.txt_json = tk.Text(self.tab_json, font=('Consolas', 8), bg='white')
        self.txt_json.pack(fill=tk.BOTH, expand=True)

        # Tab 3: Justificación
        self.tab_just = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_just, text="💡 Justificación")
        self.txt_just = tk.Text(self.tab_just, font=('Tahoma', 9), wrap=tk.WORD)
        self.txt_just.pack(fill=tk.BOTH, expand=True)

        # Tab 4: Historial
        self.tab_hist = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.tab_hist, text="📜 Historial")
        
        # Treeview para mostrar lista de análisis guardados
        cols_hist = ("fecha", "texto_resumido", "sentimiento")
        self.tree_hist = ttk.Treeview(self.tab_hist, columns=cols_hist, show="headings", height=8)
        for c in cols_hist:
            self.tree_hist.heading(c, text=c.capitalize())
            self.tree_hist.column(c, width=150 if c != "texto_resumido" else 300, anchor=tk.CENTER)
        self.tree_hist.pack(fill=tk.BOTH, expand=True)
        
        # Botones para actions de historial
        hist_btn_frame = ttk.Frame(self.tab_hist)
        hist_btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(hist_btn_frame, text="📂 Cargar Historial", command=self.cargar_historial).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(hist_btn_frame, text="🗑️ Limpiar", command=self.limpiar_historial).pack(side=tk.LEFT)

        # --- SECCIÓN 5: LEYENDA (TÍTULO CLÁSICO) ---
        legend_frame = ttk.Frame(main_container)
        legend_frame.pack(fill=tk.X, anchor=tk.W, pady=(0, 5))
        
        ttk.Label(legend_frame, text="❓ ¿Qué significa la polaridad?", font=font_bold).pack(anchor=tk.W)

        legend_text_frame = ttk.Frame(main_container, padding="2 0")
        legend_text_frame.pack(fill=tk.X)
        
        style.configure('Legend.TLabel', font=('Tahoma', 8), background=bg_color, padding=(0, 1))

        # Usar colores clásicos de XP para el texto de la leyenda
        ttk.Label(legend_text_frame, text="● POSITIVA (+0.00 a +1.00): El texto expresa emociones positivas", style='Legend.TLabel', foreground='#008000').pack(anchor=tk.W)
        ttk.Label(legend_text_frame, text="● NEGATIVA (-1.00 a -0.00): El texto expresa emociones negativas", style='Legend.TLabel', foreground='#D00000').pack(anchor=tk.W)
        ttk.Label(legend_text_frame, text="○ NEUTRAL [0.00]: El texto no muestra emociones fuertes", style='Legend.TLabel', foreground='#808080').pack(anchor=tk.W)

        # --- SECCIÓN 6: BARRA DE ESTADO INFERIOR ---
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, anchor=tk.W, pady=(5, 0))

        self.lbl_status = ttk.Label(main_container, text="Listo.")
        self.lbl_status.pack(side=tk.LEFT)
        ttk.Checkbutton(main_container, text="Auto-guardar").pack(side=tk.RIGHT)

    # def insertar_datos_ejemplo(self):
    #     # Datos de la imagen de la derecha
    #     data = [
    #         ("● Básico", "POSITIVO", "90.99%", "-"),
    #         ("○ Intermedio", "POSITIVO", "0.9", "ALTA"),
    #         ("● Avanzado", "POSITIVO", "0.9", "-")
    #     ]
        
    #     for item in data:
    #         # Insertamos los datos y aplicamos el color de fondo verde claro
    #         self.tree.insert("", tk.END, values=item, tags=('favorable',))


# --- LÓGICA FUNCIONAL ---

    def lanzar_analisis(self):
        texto = self.txt_input.get("1.0", tk.END).strip()
        if not texto: return
        
        self.btn_analizar.config(state='disabled')
        self.lbl_status.config(text="Consultando servidor LiteRT...")
        
        # Hilo para no bloquear la interfaz mientras el servidor responde
        threading.Thread(target=self.proceso_ia, args=(texto,), daemon=True).start()

    def proceso_ia(self, texto):
        """
        Orquestador del análisis que se ejecuta en un hilo secundario.
        """
        # 1. Limpieza inicial de la UI
        self.root.after(0, self.limpiar_resultados_ui)

        try:
            # --- Nivel Básico ---
            res_basico = self.analizar_fn(texto, "basico", self.provider)
            # Extraemos el valor y nos aseguramos de que sea string antes de .upper()
            sent_basico = str(res_basico.get('sentimiento', '')).upper() 
            self.root.after(0, self.insertar_en_tabla, "● Básico", sent_basico, "-", "-")

            # --- Nivel Intermedio ---
            res_intermedio = self.analizar_fn(texto, "intermedio", self.provider)
            sent_intermedio = str(res_intermedio.get('sentimiento', '')).upper()
            self.root.after(0, self.insertar_en_tabla, 
                            "○ Intermedio", 
                            sent_intermedio, 
                            res_intermedio.get('polaridad', 0), 
                            res_intermedio.get('intensidad', '-'))

            # --- Nivel Avanzado ---
            res_avanzado = self.analizar_fn(texto, "avanzado", self.provider)
            sent_avanzado = str(res_avanzado.get('sentimiento_global', '')).upper()
            self.root.after(0, self.insertar_en_tabla, 
                            "● Avanzado", 
                            sent_avanzado, 
                            res_avanzado.get('polaridad', 0), 
                            "-")

            # --- PERSISTENCIA ---
            # Dentro de proceso_ia
            self.ultimo_resultado = {
                "timestamp": datetime.now().isoformat(),
                "texto_analizado": texto,
                "niveles": {
                    "basico": res_basico,      # dict
                    "intermedio": res_intermedio,  # dict
                    "avanzado": res_avanzado    # dict
                }
            }

            # Actualizar detalles finales
            self.root.after(0, self.llenar_datos, res_avanzado)
            
        except Exception as e:
            # CORRECCIÓN AQUÍ: Capturamos el valor de 'e' en el momento del error
            # Pasamos e como un argumento por defecto (err=e) para que persista en la lambda
            error_msg = str(e) 
            self.root.after(0, lambda err=error_msg: messagebox.showerror("Error de Análisis", f"Error en la comunicación con el modelo: {err}"))
        
        finally:
            # Rehabilitar interfaz
            self.root.after(0, lambda: self.btn_analizar.config(state='normal'))
            self.root.after(0, lambda: self.lbl_status.config(text="Análisis completado."))
            
    # --- MÉTODOS DE APOYO PARA ACTUALIZAR UI DESDE EL HILO ---

    def limpiar_resultados_ui(self):
        """Limpia la tabla y los cuadros de texto."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.txt_json.delete("1.0", tk.END)
        self.txt_just.delete("1.0", tk.END)

    def insertar_en_tabla(self, nivel, sentimiento, polaridad, intensidad):
        """Inserta una fila en el Treeview con el color correspondiente."""
        # Lógica de colores XP (Verde para positivo, Rojo para negativo)
        tag = ''
        if 'POS' in sentimiento: tag = 'favorable'
        elif 'NEG' in sentimiento: tag = 'desfavorable'
        
        self.tree.insert("", tk.END, values=(nivel, sentimiento, polaridad, intensidad), tags=(tag,))



    def llenar_datos(self, analisis_avanzado):

        if analisis_avanzado:
            # 2. Llenar JSON detallado
            self.txt_json.delete("1.0", tk.END)
            self.txt_json.insert(tk.END, json.dumps(analisis_avanzado, indent=4, ensure_ascii=False))

            # 3. Llenar Justificación
            self.txt_just.delete("1.0", tk.END)
            self.txt_just.insert(tk.END, f"JUSTIFICACIÓN:\n{analisis_avanzado.get('justificacion', 'N/A')}\n\nRECOMENDACIÓN:\n{analisis_avanzado.get('recomendacion', 'N/A')}")
            
        self.lbl_status.config(text="Análisis completado.")

        # Llenar pestaña Raw Data
        self.txt_json.delete("1.0", tk.END)
        self.txt_json.insert(tk.END, json.dumps(self.ultimo_resultado, indent=4, ensure_ascii=False))
        self.lbl_status.config(text="Análisis completado.")

    def limpiar(self):
        self.txt_input.delete("1.0", tk.END)
        for item in self.tree.get_children(): self.tree.delete(item)
        self.txt_json.delete("1.0", tk.END)
        self.txt_just.delete("1.0", tk.END)

    def ejecutar_guardado(self):
        """Acción del botón GUARDAR en la interfaz XP."""
        if not hasattr(self, 'ultimo_resultado') or not self.ultimo_resultado:
            messagebox.showwarning("Atención", "Realiza un análisis antes de guardar.")
            return

        try:
            # Llamada a la función modularizada
            p_json, p_txt = guardar_resultado(self.ultimo_resultado)
            
            # Feedback al usuario
            info = f"Archivos generados correctamente:\n\n1. {os.path.basename(p_json)}\n2. {os.path.basename(p_txt)}"
            messagebox.showinfo("Sistema de Archivos", info)
            
            self.lbl_status.config(text="Resultados guardados en TXT y JSON.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

    def cargar_historial(self):
        """Carga los archivos JSON del directorio resultados/json/ y los muestra en la pestaña Historial."""
        dir_json = "resultados/json"
        if not os.path.exists(dir_json):
            messagebox.showinfo("Historial", "No hay análisis guardados aún.")
            return

        for item in self.tree_hist.get_children():
            self.tree_hist.delete(item)

        archivos = sorted(glob.glob(os.path.join(dir_json, "*.json")), reverse=True)
        
        if not archivos:
            messagebox.showinfo("Historial", "No hay análisis guardados.")
            return

        for archivo in archivos:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                
                timestamp = datos.get("timestamp", "N/A")
                texto = datos.get("texto_analizado", "")
                texto_resumido = texto[:50] + "..." if len(texto) > 50 else texto
                sent = datos.get("niveles", {}).get("basico", {}).get("sentimiento", "N/A")
                
                self.tree_hist.insert("", tk.END, values=(timestamp, texto_resumido, sent))
            except Exception:
                continue

        self.lbl_status.config(text=f"Historial cargado: {len(archivos)} análisis.")

    def limpiar_historial(self):
        """Limpia la pestaña de historial."""
        for item in self.tree_hist.get_children():
            self.tree_hist.delete(item)
        self.lbl_status.config(text="Historial limpiado.")