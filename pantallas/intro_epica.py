# pantallas/intro_epica.py
import tkinter as tk

class PantallaIntroEpica:
    """Pantalla de introducción épica"""
    
    def __init__(self, app_principal, callback_finalizar, root):
        self.app = app_principal
        self.callback_finalizar = callback_finalizar
        self.root = root
        self.ventana = None
        self.canvas = None
        
        print("🎬 Creando introducción épica...")
        self._crear_interfaz()
        self._iniciar_secuencia()
    
    def _crear_interfaz(self):
        """Crea la pantalla de introducción"""
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Planificador Imperial Romano")
        
        # Pantalla completa
        self.ventana.attributes('-fullscreen', True)
        self.ventana.configure(bg='black')
        self.ventana.overrideredirect(True)
        
        # Canvas para animaciones
        self.canvas = tk.Canvas(self.ventana, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Configurar tecla de escape
        self.ventana.bind('<Escape>', lambda e: self._saltar_intro())
    
    def _iniciar_secuencia(self):
        """Inicia la secuencia de introducción"""
        
        # Título
        self.canvas.create_text(
            self.ventana.winfo_screenwidth() // 2,
            self.ventana.winfo_screenheight() // 2 - 50,
            text="SENATUS POPULUSQUE ROMANUS",
            font=("Times New Roman", 48, "bold"),
            fill="#d4af37",
            tags="titulo"
        )
        
        # Subtítulo
        self.ventana.after(1500, self._mostrar_subtitulo)
        
        # Lema
        self.ventana.after(3000, self._mostrar_lema)
        
        # Contador
        self.ventana.after(4500, self._iniciar_contador)
    
    def _mostrar_subtitulo(self):
        """Muestra el subtítulo"""
        self.canvas.create_text(
            self.ventana.winfo_screenwidth() // 2,
            self.ventana.winfo_screenheight() // 2 + 30,
            text="PLANIFICADOR IMPERIAL",
            font=("Garamond", 32, "italic"),
            fill="#c0c0c0",
            tags="subtitulo"
        )
    
    def _mostrar_lema(self):
        """Muestra el lema romano"""
        self.canvas.create_text(
            self.ventana.winfo_screenwidth() // 2,
            self.ventana.winfo_screenheight() // 2 + 100,
            text="DIVIDE ET IMPERA",
            font=("Arial", 28, "bold"),
            fill="#8b7355",
            tags="lema"
        )
    
    def _iniciar_contador(self):
        """Inicia el contador para finalizar intro"""
        self.contador = 3
        
        self.contador_texto = self.canvas.create_text(
            self.ventana.winfo_screenwidth() - 100,
            50,
            text=f"Comienza en: {self.contador}",
            font=("Arial", 16),
            fill="#666666",
            tags="contador"
        )
        
        self._actualizar_contador()
    
    def _actualizar_contador(self):
        """Actualiza el contador"""
        if self.contador > 0:
            self.canvas.itemconfig("contador", text=f"Comienza en: {self.contador}")
            self.contador -= 1
            self.ventana.after(1000, self._actualizar_contador)
        else:
            self._finalizar_intro()
    
    def _finalizar_intro(self):
        """Finaliza la introducción"""
        self.ventana.destroy()
        if self.callback_finalizar:
            self.callback_finalizar()
    
    def _saltar_intro(self):
        """Permite saltar la intro con ESC"""
        self.ventana.destroy()
        if self.callback_finalizar:
            self.callback_finalizar()
    
    def destruir(self):
        """Limpia los recursos"""
        try:
            if self.ventana:
                self.ventana.destroy()
        except:
            pass