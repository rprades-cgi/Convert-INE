"""
Módulo de interfaz gráfica para el convertidor INE
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from converter_core import convertir_fichero_vias


class StreetFormatConverterGUI:
    """Interfaz gráfica del convertidor INE"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Convertidor INE - Formato de Vías")
        self.root.geometry("500x400")
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Convertidor de Formato INE", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de archivo de entrada
        ttk.Label(main_frame, text="Archivo de entrada:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=40, state="readonly").grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Examinar", command=self.select_input_file).grid(row=1, column=2)
        
        # Selección de archivo de salida
        ttk.Label(main_frame, text="Archivo de salida:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=40, state="readonly").grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Examinar", command=self.select_output_file).grid(row=2, column=2)
        
        # Barra de progreso
        ttk.Label(main_frame, text="Progreso:").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(20, 5))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Convertir", command=self.convert_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Área de texto para logs
        ttk.Label(main_frame, text="Log de conversión:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=8, width=60)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        main_frame.rowconfigure(6, weight=1)
        
    def log_message(self, message: str):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def select_input_file(self):
        """Seleccionar archivo de entrada"""
        filetypes = [
            ("Archivos de Vías INE", "VIAS.*"),
            ("Archivos de texto", "*.txt"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecciona el fichero de VIAS (cualquier formato INE)",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file.set(filename)
            # Generar nombre de salida automáticamente
            output_name = self._generate_output_filename(filename)
            self.output_file.set(output_name)
            self.log_message(f"Archivo de entrada seleccionado: {os.path.basename(filename)}")
            self.log_message(f"Archivo de salida: {os.path.basename(output_name)}")
    
    def _generate_output_filename(self, input_filename: str) -> str:
        """Generar nombre de archivo de salida automáticamente"""
        base, ext = os.path.splitext(input_filename)
        
        # Manejar diferentes formatos de archivo INE
        if ".P02." in base.upper() or ".P28." in base.upper():
            # Para archivos con formato INE, eliminar la parte de fecha
            parts = base.split('.')
            if len(parts) >= 3 and parts[1].upper() in ['P02', 'P28']:
                # Mantener solo la parte base (ej: VIAS.P02.D250630.G250702 -> VIAS)
                base = parts[0]
        
        return base + "_convertido.txt"
    
    def select_output_file(self):
        """Seleccionar archivo de salida"""
        filename = filedialog.asksaveasfilename(
            title="Guardar archivo convertido como",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            self.output_file.set(filename)
            self.log_message(f"Archivo de salida seleccionado: {os.path.basename(filename)}")
    
    def clear_form(self):
        """Limpiar formulario"""
        self.input_file.set("")
        self.output_file.set("")
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        self.log_message("Formulario limpiado")
    
    def update_progress(self, lineas_procesadas: int, lineas_totales: int):
        """Actualizar barra de progreso"""
        progress = (lineas_procesadas / lineas_totales) * 100
        self.progress_var.set(progress)
        self.root.update_idletasks()
        
        if lineas_procesadas % 100 == 0:
            self.log_message(f"Procesadas {lineas_procesadas}/{lineas_totales} líneas...")
    
    def convert_file(self):
        """Convertir archivo"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo de entrada")
            return
            
        if not self.output_file.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo de salida")
            return
        
        try:
            self.log_message("Iniciando conversión...")
            errores = convertir_fichero_vias(
                self.input_file.get(), 
                self.output_file.get(),
                callback_progreso=self.update_progress,
                callback_log=self.log_message
            )
            
            if errores:
                mensaje = f"Se encontraron {len(errores)} errores en el fichero:\n\n"
                mensaje += "\n".join(errores[:10])
                if len(errores) > 10:
                    mensaje += f"\n... y {len(errores) - 10} más."
                
                self.log_message(f"Conversión completada con {len(errores)} errores")
                messagebox.showwarning("Verificación con errores", mensaje)
            else:
                self.log_message("Conversión completada sin errores")
                messagebox.showinfo("Conversión completada",
                                  f"El fichero se ha convertido correctamente.\n\n"
                                  f"Fichero generado:\n{self.output_file.get()}")
                
        except Exception as e:
            error_msg = f"Error durante la conversión: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.log_message("Aplicación iniciada")
        self.root.mainloop()


def main():
    """Función principal para ejecutar la GUI"""
    app = StreetFormatConverterGUI()
    app.run()
