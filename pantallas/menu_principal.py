# pantallas/menu_principal.py
import tkinter as tk
from tkinter import messagebox

class PantallaMenuPrincipal:
    """Pantalla del menú principal"""
    
    def __init__(self, app_principal, root):
        self.app = app_principal
        self.root = root
        self.ventana = None
        
        print("🏠 Creando menú principal...")
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz del menú principal"""
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Planificador del Imperio Romano - Menú Principal")
        self.ventana.attributes('-fullscreen', True)
        self.ventana.configure(bg="#1a1a1a")
        
        # Centrar ventana
        self._centrar_ventana()
        
        # Configurar protocolo de cierre
        self.ventana.protocol("WM_DELETE_WINDOW", self._confirmar_salida)
        
        # Crear contenido
        self._crear_contenido()
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = 900
        alto = 700
        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def _crear_contenido(self):
        """Crea todo el contenido del menú"""
        
        # TÍTULO PRINCIPAL
        titulo_frame = tk.Frame(self.ventana, bg="#1a1a1a")
        titulo_frame.pack(fill="x", pady=(40, 20))
        
        tk.Label(
            titulo_frame,
            text="PLANIFICADOR IMPERIAL ROMANO",
            font=("Times New Roman", 36, "bold"),
            fg="#d4af37",
            bg="#1a1a1a"
        ).pack()
        
        tk.Label(
            titulo_frame,
            text="Menú Principal",
            font=("Garamond", 18, "italic"),
            fg="#c0c0c0",
            bg="#1a1a1a"
        ).pack(pady=(10, 0))
        
        # LÍNEA DECORATIVA
        linea = tk.Frame(self.ventana, height=2, bg="#8b7355")
        linea.pack(fill="x", padx=100, pady=20)
        
        # FRAME PARA OPCIONES
        opciones_frame = tk.Frame(self.ventana, bg="#1a1a1a")
        opciones_frame.pack(fill="both", expand=True, padx=150, pady=20)
        
        # BOTONES DE OPCIÓN
        opciones = [
            ("📅", "GESTIONAR EVENTOS", self._abrir_gestion_eventos, "#8b0000"),
            ("🏛️", "CONVOCAR SENADO", self._convocar_senado, "#0a3d62"),
            ("📊", "VER ESTADÍSTICAS", self._ver_estadisticas, "#006400"),
            ("⚙️", "CONFIGURACIÓN", self._abrir_configuracion, "#8b7355"),
            ("❌", "SALIR", self._confirmar_salida, "#333333")
        ]
        
        for emoji, texto, comando, color in opciones:
            self._crear_boton_opcion(opciones_frame, emoji, texto, comando, color)
    
    def _crear_boton_opcion(self, parent, emoji, texto, comando, color):
        """Crea un botón de opción del menú"""
        btn_frame = tk.Frame(parent, bg="#1a1a1a")
        btn_frame.pack(fill="x", pady=12)
        
        btn = tk.Button(
            btn_frame,
            text=f"  {emoji}  {texto}",
            command=comando,
            font=("Arial", 16, "bold"),
            bg=color,
            fg="white",
            activebackground=self._aclarar_color(color),
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            width=30,
            height=2,
            anchor="w",
            padx=20
        )
        btn.pack()
        
        def on_enter(e):
            btn.config(bg=self._aclarar_color(color))
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _aclarar_color(self, hex_color):
        """Aclara un color hexadecimal"""
        r = min(int(hex_color[1:3], 16) + 20, 255)
        g = min(int(hex_color[3:5], 16) + 20, 255)
        b = min(int(hex_color[5:7], 16) + 20, 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _abrir_gestion_eventos(self):
        """Abre la pantalla de gestión de eventos"""
        print("📅 Abriendo gestión de eventos...")
        
        try:
            self.ventana.destroy()
        except:
            pass
        
        try:
            self.app.mostrar_gestion_eventos()
        except Exception as e:
            print(f"Error al abrir gestión de eventos: {e}")
            self.app.mostrar_menu()
    
    def _convocar_senado(self):
        """Convocar al senado"""
        respuesta = messagebox.askyesno(
            "Convocar Senado",
            "¿Desea convocar una sesión extraordinaria del Senado?",
            parent=self.ventana
        )
        
        if respuesta:
            messagebox.showinfo(
                "Senado Convocado",
                "✅ El Senado ha sido oficialmente convocado.",
                parent=self.ventana
            )
            self.app.convocar_senado()
    
    def _ver_estadisticas(self):
        """Muestra estadísticas"""
        self.app.mostrar_estadisticas()
    
    def _abrir_configuracion(self):
        """Abre configuración"""
        self.app.mostrar_configuracion()
    
    def _confirmar_salida(self):
        """Confirma si el usuario quiere salir"""
        respuesta = messagebox.askyesno(
            "Salir",
            "¿Está seguro de que desea salir del Planificador Imperial?",
            parent=self.ventana
        )
        
        if respuesta:
            print("👋 Usuario confirmó salida...")
            self.ventana.destroy()
            self.app.salir_aplicacion()
    
    def destruir(self):
        """Limpia los recursos de esta pantalla"""
        try:
            if self.ventana and self.ventana.winfo_exists():
                self.ventana.destroy()
        except:
            pass