import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class PlanificadorRomanoApp:
    """Aplicación principal del Planificador Imperial Romano"""
    
    def __init__(self):
        
        # Configurar directorio actual
        self.dir_actual = os.path.dirname(os.path.abspath(__file__))
        self.directorio_datos = os.path.join(self.dir_actual, "datos")
        
        # VENTANA PRINCIPAL TK (SOLO UNA VEZ)
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal
        self.root.title("Planificador Imperial Romano")
        
        # Cargar módulos
        self._cargar_modulos()
        
        # Inicializar componentes
        self._inicializar_componentes()
        
    
    def _cargar_modulos(self):
        
        # MODELOS
        try:
            from modelos.evento import Evento
            self.Evento = Evento
            print(" modelos.evento.Evento")
        except ImportError as e:
            print(f" Error importando Evento: {e}")
            class Evento:
                def __init__(self, nombre, inicio, fin, recursos=None):
                    self.nombre = nombre
                    self.inicio = inicio
                    self.fin = fin
                    self.recursos = recursos if recursos else []
            self.Evento = Evento
        
        try:
            from modelos.recurso import Recurso
            self.Recurso = Recurso
            print(" modelos.recurso.Recurso")
        except ImportError as e:
            print(f" Error importando Recurso: {e}")
            self.Recurso = None
        
        # NUCLEO
        try:
            from nucleo.calendario import Calendario
            self.Calendario = Calendario
            print(" nucleo.calendario.Calendario")
        except ImportError as e:
            print(f" Error importando Calendario: {e}")
            class Calendario:
                def __init__(self):
                    self.eventos = []
                def agregar_evento(self, evento):
                    self.eventos.append(evento)
                def listar_eventos(self):
                    return self.eventos
            self.Calendario = Calendario
        
        try:
            from nucleo.persistencia import Persistencia
            self.Persistencia = Persistencia
            print(" nucleo.persistencia.Persistencia")
        except ImportError as e:
            print(f" Error importando Persistencia: {e}")
        
        try:
            from nucleo.buscador import Buscador
            self.Buscador = Buscador
            print(" nucleo.buscador.Buscador")
        except ImportError as e:
            print(f" Error importando Buscador: {e}")
        
        # PANTALLAS
        self.pantallas_cargadas = {}
        try:
            from pantallas.intro_epica import PantallaIntroEpica
            self.PantallaIntroEpica = PantallaIntroEpica
            self.pantallas_cargadas['intro'] = True
            print(" pantallas.intro_epica.PantallaIntroEpica")
        except ImportError as e:
            print(f" No se pudo cargar intro_epica: {e}")
            self.pantallas_cargadas['intro'] = False
        
        try:
            from pantallas.menu_principal import PantallaMenuPrincipal
            self.PantallaMenuPrincipal = PantallaMenuPrincipal
            self.pantallas_cargadas['menu'] = True
            print(" pantallas.menu_principal.PantallaMenuPrincipal")
        except ImportError as e:
            print(f" No se pudo cargar menu_principal: {e}")
            self.pantallas_cargadas['menu'] = False
        
        try:
            from pantallas.gestion_eventos import PantallaGestionEventos
            self.PantallaGestionEventos = PantallaGestionEventos
            self.pantallas_cargadas['eventos'] = True
            print(" pantallas.gestion_eventos.PantallaGestionEventos")
        except ImportError as e:
            print(f" No se pudo cargar gestion_eventos: {e}")
            self.pantallas_cargadas['eventos'] = False
    
    def _inicializar_componentes(self):
        """Inicializa todos los componentes de la aplicación"""
        # Crear calendario con directorio de datos
        self.calendario = self.Calendario(directorio_datos=self.directorio_datos)
        
        # Inicializar recursos
        self._inicializar_recursos()
        
        # Variables de estado
        self.ventana_actual = None
    
    def _inicializar_recursos(self):
        """Inicializa recursos por defecto"""
        if self.Recurso:
            try:
                # Inicializar recursos (cargará desde archivo si existe)
                self.Recurso.inicializar(self.directorio_datos)
                
                # Si no hay recursos, crear los iniciales
                if len(self.Recurso.obtener_todos()) == 0:
                    recursos_iniciales = [
                        "Legionarios", 
                        "Centuriones", 
                        "Soldados de Caballería",
                        "Monedas de Oro", 
                        "Armaduras",
                        "Espadas", 
                        "Escudos", 
                        "Catapultas", 
                        "Ballestas",
                        "Provisiones", 
                        "Caballos"
                    ]
                    
                    for recurso in recursos_iniciales:
                        self.Recurso.agregar_recurso(recurso)
                    
                    print(f" {len(recursos_iniciales)} recursos iniciales creados")
                else:
                    print(f" {len(self.Recurso.obtener_todos())} recursos cargados desde archivo")
                    
                print(f"   Recursos disponibles: {len(self.Recurso.obtener_disponibles())}/{len(self.Recurso.obtener_todos())}")
                
            except Exception as e:
                print(f" Error inicializando recursos: {e}")
    
    def iniciar(self):
        """Punto de entrada principal"""
        print("\n▶ INICIANDO PLANIFICADOR IMPERIAL...")
        
        if self.pantallas_cargadas.get('intro', False):
            self.mostrar_intro()
        else:
            self.mostrar_menu()
        
        # INICIAR MAINLOOP (SOLO UNA VEZ)
        self.root.mainloop()
    
    def mostrar_intro(self):
        """Muestra la pantalla de introducción"""
        print(" Mostrando introducción épica...")
        
        try:
            self.ventana_actual = self.PantallaIntroEpica(
                app_principal=self,
                callback_finalizar=self.mostrar_menu,
                root=self.root
            )
        except Exception as e:
            print(f" Error mostrando intro: {e}")
            self.mostrar_menu()
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print(" Mostrando menú principal...")
        
        if not self.pantallas_cargadas.get('menu'):
            print(" Menú no disponible")
            return
        
        try:
            # Cerrar ventana actual si existe
            if self.ventana_actual:
                try:
                    if hasattr(self.ventana_actual, 'destruir'):
                        self.ventana_actual.destruir()
                except Exception as e:
                    print(f" Error cerrando ventana anterior: {e}")
            
            self.ventana_actual = self.PantallaMenuPrincipal(
                app_principal=self,
                root=self.root
            )
        except Exception as e:
            print(f" Error mostrando menú: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_gestion_eventos(self):
        """Muestra la gestión de eventos"""
        print(" Mostrando gestión de eventos...")
        
        if not self.pantallas_cargadas.get('eventos'):
            print(" Gestión de eventos no disponible")
            return
        
        try:
            # Cerrar ventana actual si existe
            if self.ventana_actual:
                try:
                    if hasattr(self.ventana_actual, 'destruir'):
                        self.ventana_actual.destruir()
                except Exception as e:
                    print(f" Error cerrando ventana anterior: {e}")
            
            self.ventana_actual = self.PantallaGestionEventos(
                app_principal=self,
                calendario=self.calendario,
                root=self.root
            )
            
            print(" Pantalla de eventos creada")
            
        except Exception as e:
            print(f" Error mostrando eventos: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_menu()
    
    def convocar_senado(self):
        """Convocar al senado"""
        messagebox.showinfo("Senado", " ¡Senado convocado!\n\nQue comience el debate imperial.")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas avanzadas usando el Buscador"""
        try:
            informe = self.calendario.generar_informe()
            
            mensaje = (
                f"📊 INFORME IMPERIAL 📊\n"
                f"{'='*40}\n"
                f"📅 Eventos totales: {informe['total_eventos']}\n"
                f"⏳ Eventos en curso: {informe['eventos_en_curso']}\n"
                f"🔜 Próximos (7 días):{informe['eventos_proximos_7_dias']}\n"
                f"📜 Eventos pasados: {informe['eventos_pasados']}\n"
                f"⚔️ Eventos sin recursos: {informe['eventos_sin_recursos']}\n"
            )
            
            # Agregar recursos más usados
            if informe['estadisticas_recursos']:
                mensaje += f"\n📈 RECURSOS MÁS UTILIZADOS:\n"
                items = list(informe['estadisticas_recursos'].items())[:5]
                for recurso, cantidad in items:
                    mensaje += f"  • {recurso}: {cantidad} eventos\n"
            
            # Agregar conteo por mes
            if informe['conteo_por_mes']:
                mensaje += f"\n EVENTOS POR MES:\n"
                for mes, cantidad in list(informe['conteo_por_mes'].items())[:6]:
                    mensaje += f"  • {mes}: {cantidad} eventos\n"
            
            messagebox.showinfo("Estadísticas Imperiales", mensaje)
            
        except Exception as e:
            print(f"Error generando informe: {e}")
            # Versión simple si falla
            total = len(self.calendario.eventos)
            messagebox.showinfo("Estadísticas", f" Eventos totales: {total}")
    
    def mostrar_configuracion(self):
        """Muestra configuración con opciones avanzadas"""
        opciones = (
            "⚙️ CONFIGURACIÓN IMPERIAL\n\n"
            "1. Información del sistema\n"
            "2. Exportar datos\n"
            "3. Importar datos\n"
            "4. Limpiar todos los datos\n"
            "5. Acerca de\n"
            "6. Volver"
        )
        
        respuesta = simpledialog.askstring(
            "Configuración Imperial",
            opciones + "\n\nSeleccione una opción (1-6):",
            parent=self.root
        )
        
        if respuesta == "1":
            self._mostrar_info_sistema()
        elif respuesta == "2":
            self._exportar_datos()
        elif respuesta == "3":
            self._importar_datos()
        elif respuesta == "4":
            self._limpiar_datos()
        elif respuesta == "5":
            self._acerca_de()
    
    def _mostrar_info_sistema(self):
        """Muestra información del sistema"""
        import platform
        
        info = (
            f"💻 INFORMACIÓN DEL SISTEMA\n"
            f"{'='*30}\n"
            f"Sistema: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}\n"
            f"Procesador: {platform.processor()}\n"
            f"{'='*30}\n"
            f" Directorio datos: {self.directorio_datos}\n"
            f" Eventos cargados: {len(self.calendario.eventos)}\n"
        )
        
        # Estadísticas de datos
        try:
            stats = self.calendario.obtener_estadisticas_datos()
            if stats['existe']:
                info += f" Archivos de datos: {len(stats['archivos'])}\n"
                for archivo in stats['archivos']:
                    info += f"  • {archivo['nombre']}: {archivo['tamaño_kb']:.1f} KB\n"
        except:
            pass
        
        messagebox.showinfo("Información del Sistema", info)
    
    def _exportar_datos(self):
        """Exporta datos a otra ubicación"""
        from tkinter import filedialog
        
        destino = filedialog.askdirectory(
            title="Seleccionar carpeta destino para exportar",
            parent=self.root
        )
        
        if destino:
            try:
                resultado = self.calendario.exportar_datos(destino)
                if resultado:
                    messagebox.showinfo(
                        "Exportación exitosa",
                        f" Datos exportados a:\n{destino}\n\n"
                        f"Archivos exportados: {', '.join(resultado)}"
                    )
                else:
                    messagebox.showwarning(
                        "Sin datos",
                        "No hay datos para exportar."
                    )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")
    
    def _importar_datos(self):
        """Importa datos desde otra ubicación"""
        from tkinter import filedialog
        
        origen = filedialog.askdirectory(
            title="Seleccionar carpeta con datos para importar",
            parent=self.root
        )
        
        if origen:
            respuesta = messagebox.askyesno(
                "Confirmar importación",
                "¿Importar datos? Esto sobrescribirá los datos actuales."
            )
            
            if respuesta:
                try:
                    resultado = self.calendario.importar_datos(origen)
                    if resultado:
                        # Recargar datos
                        self.calendario.cargar_eventos()
                        if self.Recurso:
                            self.Recurso.inicializar(self.directorio_datos)
                        
                        messagebox.showinfo(
                            "Importación exitosa",
                            f" Datos importados desde:\n{origen}\n\n"
                            f"Archivos importados: {', '.join(resultado)}\n"
                            f"Eventos cargados: {len(self.calendario.eventos)}"
                        )
                    else:
                        messagebox.showwarning(
                            "Sin datos",
                            "No se encontraron datos para importar."
                        )
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo importar: {e}")
    
    def _limpiar_datos(self):
        """Limpia todos los datos"""
        respuesta = messagebox.askyesno(
            "Confirmar limpieza",
            "⚠️ ¿ESTÁ SEGURO de que desea limpiar TODOS los datos?\n\n"
            "Esta acción:\n"
            "• Eliminará todos los eventos\n"
            "• Eliminará todos los recursos\n"
            "• NO se puede deshacer\n\n"
            "¿Continuar?"
        )
        
        if respuesta:
            try:
                archivos_eliminados = self.calendario.limpiar_datos()
                
                # Reinicializar recursos
                if self.Recurso:
                    self.Recurso.inicializar(self.directorio_datos)
                    self._inicializar_recursos()
                
                messagebox.showinfo(
                    "Limpieza completada",
                    f"✅ {archivos_eliminados} archivos eliminados\n\n"
                    f"El sistema se ha reinicializado."
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo limpiar datos: {e}")
    
    def _acerca_de(self):
        """Muestra información acerca de la aplicación"""
        info = (
            f"🏛️ PLANIFICADOR IMPERIAL ROMANO\n"
            f"{'='*30}\n"
            f"Versión: 2.0 (Edición Imperial)\n"
            f"Desarrollado para: Senatus Populusque Romanus\n\n"
            f"Características:\n"
            f"• Gestión completa de eventos\n"
            f"• Sistema de recursos romanos\n"
            f"• Persistencia automática\n"
            f"• Búsqueda avanzada\n"
            f"• Estadísticas imperiales\n\n"
            f"© 2024 - Todos los derechos reservados\n"
            f"¡Ave César!"
        )
        
        messagebox.showinfo("Acerca de", info)
    
    def salir_aplicacion(self):
        """Cierra la aplicación guardando todo"""
        print("\n👋 Saliendo del Planificador Imperial...")
        
        # Guardar todos los datos antes de salir
        try:
            self.calendario.guardar_eventos()
            
            if self.Recurso and hasattr(self.Recurso, 'guardar_estado'):
                self.Recurso.guardar_estado()
                
            print("💾 Datos imperiales guardados correctamente")
            print(f"📁 Ubicación: {self.directorio_datos}")
        except Exception as e:
            print(f"⚠️ Error guardando datos: {e}")
        
        print("⚔️ ¡Hasta la próxima, César!")
        self.root.quit()
        self.root.destroy()
        