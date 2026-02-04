# pantallas/gestion_eventos.py
import tkinter as tk
from tkinter import messagebox, ttk

class PantallaGestionEventos:
    """Pantalla para gestionar eventos"""
    
    def __init__(self, app_principal, calendario, root):
        self.app = app_principal
        self.calendario = calendario
        self.root = root
        self.ventana = None
        
        print("📝 Creando pantalla de gestión de eventos...")
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de gestión de eventos"""
        self.ventana = tk.Toplevel(self.root)
        self.ventana.title("Planificador Romano - Gestión de Eventos")
        self.ventana.geometry("1100x750")
        self.ventana.configure(bg="#2b2b2b")
        
        # Centrar ventana
        self._centrar_ventana()
        
        # Configurar cierre
        self.ventana.protocol("WM_DELETE_WINDOW", lambda: self._volver_al_menu())
        
        # Crear interfaz
        self._crear_encabezado()
        self._crear_formulario()
        self._crear_lista_eventos()
        self._crear_botones()
        self._crear_pie()
        
        # Cargar eventos existentes
        self._cargar_eventos()
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = 1100
        alto = 750
        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def _crear_encabezado(self):
        """Crea el encabezado de la pantalla"""
        encabezado_frame = tk.Frame(self.ventana, bg="#1a1a1a")
        encabezado_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            encabezado_frame,
            text="📅 GESTIÓN DE EVENTOS IMPERIALES",
            font=("Times New Roman", 28, "bold"),
            fg="#d4af37",
            bg="#1a1a1a"
        ).pack(pady=15)
        
        btn_volver = tk.Button(
            encabezado_frame,
            text="← Volver al Menú",
            command=self._volver_al_menu,
            font=("Arial", 10),
            bg="#333333",
            fg="white",
            cursor="hand2"
        )
        btn_volver.pack(side="left", padx=20, pady=5)
    
    def _crear_formulario(self):
        """Crea el formulario para agregar eventos"""
        formulario_frame = tk.LabelFrame(
            self.ventana,
            text=" NUEVO EVENTO IMPERIAL ",
            font=("Arial", 12, "bold"),
            fg="#d4af37",
            bg="#3a3a3a",
            relief=tk.GROOVE,
            bd=2
        )
        formulario_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        campos_frame = tk.Frame(formulario_frame, bg="#3a3a3a")
        campos_frame.pack(padx=20, pady=20)
        
        # Campo Nombre
        tk.Label(
            campos_frame,
            text="Nombre del Evento:",
            font=("Arial", 10),
            fg="white",
            bg="#3a3a3a"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        
        self.entry_nombre = tk.Entry(
            campos_frame,
            width=40,
            font=("Arial", 10),
            bg="white"
        )
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=8)
        
        # Campo Fecha Inicio
        tk.Label(
            campos_frame,
            text="Fecha Inicio (DD/MM/AAAA):",
            font=("Arial", 10),
            fg="white",
            bg="#3a3a3a"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        
        self.entry_inicio = tk.Entry(
            campos_frame,
            width=20,
            font=("Arial", 10),
            bg="white"
        )
        self.entry_inicio.grid(row=1, column=1, sticky="w", padx=5, pady=8)
        
        # Campo Fecha Fin
        tk.Label(
            campos_frame,
            text="Fecha Fin (DD/MM/AAAA):",
            font=("Arial", 10),
            fg="white",
            bg="#3a3a3a"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        
        self.entry_fin = tk.Entry(
            campos_frame,
            width=20,
            font=("Arial", 10),
            bg="white"
        )
        self.entry_fin.grid(row=2, column=1, sticky="w", padx=5, pady=8)
        
        # Frame para recursos
        recursos_frame = tk.Frame(campos_frame, bg="#3a3a3a")
        recursos_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=8)
        
        # Lista de recursos seleccionados
        tk.Label(
            recursos_frame,
            text="Recursos seleccionados:",
            font=("Arial", 10),
            fg="white",
            bg="#3a3a3a"
        ).grid(row=0, column=0, sticky="w", padx=5)
        
        self.lista_recursos_seleccionados = tk.Listbox(
            recursos_frame,
            width=35,
            height=3,
            font=("Arial", 9),
            bg="#f0f0f0"
        )
        self.lista_recursos_seleccionados.grid(row=1, column=0, padx=5, pady=5)
        
        # Frame para controles de recursos
        controles_frame = tk.Frame(recursos_frame, bg="#3a3a3a")
        controles_frame.grid(row=1, column=1, padx=10, sticky="n")
        
        # Combobox para seleccionar recursos disponibles
        tk.Label(
            controles_frame,
            text="Recursos disponibles:",
            font=("Arial", 9),
            fg="white",
            bg="#3a3a3a"
        ).pack(anchor="w")
        
        self.combo_recursos = ttk.Combobox(
            controles_frame,
            width=20,
            font=("Arial", 9),
            state="readonly"
        )
        self.combo_recursos.pack(pady=(0, 5))
        
        # Botón para agregar recurso
        btn_agregar_recurso = tk.Button(
            controles_frame,
            text="+ Agregar",
            command=self._agregar_recurso_a_lista,
            font=("Arial", 9),
            bg="#5a452d",
            fg="white",
            cursor="hand2",
            width=12
        )
        btn_agregar_recurso.pack(pady=2)
        
        # Botón para quitar recurso
        btn_quitar_recurso = tk.Button(
            controles_frame,
            text="- Quitar",
            command=self._quitar_recurso_de_lista,
            font=("Arial", 9),
            bg="#8b0000",
            fg="white",
            cursor="hand2",
            width=12
        )
        btn_quitar_recurso.pack(pady=2)
        
        # Botón para nuevo recurso
        btn_nuevo_recurso = tk.Button(
            controles_frame,
            text="+ Nuevo Recurso",
            command=self._nuevo_recurso_dialogo,
            font=("Arial", 9),
            bg="#006400",
            fg="white",
            cursor="hand2",
            width=12
        )
        btn_nuevo_recurso.pack(pady=2)
        
        # Actualizar lista de recursos disponibles
        self._actualizar_recursos_disponibles()
        
        # Botón agregar evento
        btn_agregar = tk.Button(
            campos_frame,
            text="➕ AGREGAR EVENTO",
            command=self._agregar_evento,
            font=("Arial", 11, "bold"),
            bg="#8b0000",
            fg="white",
            cursor="hand2",
            width=20
        )
        btn_agregar.grid(row=4, column=0, columnspan=2, pady=15)
    
    def _crear_lista_eventos(self):
        """Crea la lista/tabla de eventos"""
        lista_frame = tk.LabelFrame(
            self.ventana,
            text=" EVENTOS REGISTRADOS ",
            font=("Arial", 12, "bold"),
            fg="#d4af37",
            bg="#3a3a3a",
            relief=tk.GROOVE,
            bd=2
        )
        lista_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scroll_y = tk.Scrollbar(lista_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(lista_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(
            lista_frame,
            columns=("ID", "Nombre", "Inicio", "Fin", "Recursos"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=12
        )
        
        self.tree.heading("ID", text="#")
        self.tree.heading("Nombre", text="📄 Evento")
        self.tree.heading("Inicio", text="📅 Inicio")
        self.tree.heading("Fin", text="🏁 Fin")
        self.tree.heading("Recursos", text="⚔️ Recursos")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Inicio", width=100, anchor="center")
        self.tree.column("Fin", width=100, anchor="center")
        self.tree.column("Recursos", width=250)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.contador_label = tk.Label(
            lista_frame,
            text="Eventos: 0",
            font=("Arial", 10, "bold"),
            fg="#d4af37",
            bg="#3a3a3a"
        )
        self.contador_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def _crear_botones(self):
        """Crea botones de acción"""
        botones_frame = tk.Frame(self.ventana, bg="#2b2b2b")
        botones_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_eliminar = tk.Button(
            botones_frame,
            text="🗑️ ELIMINAR SELECCIONADO",
            command=self._eliminar_evento,
            font=("Arial", 10),
            bg="#8b0000",
            fg="white",
            cursor="hand2"
        )
        btn_eliminar.pack(side="left", padx=5)
        
        btn_limpiar = tk.Button(
            botones_frame,
            text="🔄 ACTUALIZAR LISTA",
            command=self._actualizar_lista,
            font=("Arial", 10),
            bg="#006400",
            fg="white",
            cursor="hand2"
        )
        btn_limpiar.pack(side="left", padx=5)
        
        btn_limpiar_campos = tk.Button(
            botones_frame,
            text="📝 LIMPIAR CAMPOS",
            command=self._limpiar_campos,
            font=("Arial", 10),
            bg="#5a452d",
            fg="white",
            cursor="hand2"
        )
        btn_limpiar_campos.pack(side="left", padx=5)
        
        btn_senado = tk.Button(
            botones_frame,
            text="🏛️ CONVOCAR SENADO",
            command=self._convocar_senado,
            font=("Arial", 10),
            bg="#0a3d62",
            fg="white",
            cursor="hand2"
        )
        btn_senado.pack(side="right", padx=5)
    
    def _crear_pie(self):
        """Crea el pie de página"""
        pie_frame = tk.Frame(self.ventana, bg="#1a1a1a")
        pie_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        tk.Frame(pie_frame, height=1, bg="#8b7355").pack(fill="x", padx=20, pady=(0, 10))
        
        tk.Label(
            pie_frame,
            text="© Senatus Populusque Romanus - Sistema de Gestión Imperial v1.0",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a1a"
        ).pack()
    
    def _actualizar_recursos_disponibles(self):
        """Actualiza la lista de recursos disponibles"""
        try:
            from modelos.recurso import Recurso
            disponibles = Recurso.obtener_disponibles()
            
            # Mostrar disponibles en combobox
            self.combo_recursos['values'] = disponibles
            
            if disponibles:
                self.combo_recursos.set(disponibles[0])
            else:
                self.combo_recursos.set("No hay disponibles")
                
        except ImportError:
            self.combo_recursos['values'] = []
            self.combo_recursos.set("Error cargando recursos")
    
    def _agregar_recurso_a_lista(self):
        """Agrega el recurso seleccionado a la lista"""
        recurso = self.combo_recursos.get()
        if recurso and recurso != "No hay disponibles":
            # Verificar que no esté ya en la lista
            items = list(self.lista_recursos_seleccionados.get(0, tk.END))
            if recurso not in items:
                self.lista_recursos_seleccionados.insert(tk.END, recurso)
    
    def _quitar_recurso_de_lista(self):
        """Quita el recurso seleccionado de la lista"""
        seleccion = self.lista_recursos_seleccionados.curselection()
        if seleccion:
            self.lista_recursos_seleccionados.delete(seleccion[0])
    
    def _nuevo_recurso_dialogo(self):
        """Diálogo para agregar nuevo recurso"""
        nuevo = messagebox.askstring(
            "Nuevo Recurso",
            "Ingrese nombre del nuevo recurso:",
            parent=self.ventana
        )
        
        if nuevo and nuevo.strip():
            try:
                from modelos.recurso import Recurso
                if Recurso.agregar_recurso(nuevo.strip()):
                    self._actualizar_recursos_disponibles()
                    messagebox.showinfo(
                        "Recurso agregado",
                        f"✅ Recurso '{nuevo}' agregado al sistema",
                        parent=self.ventana
                    )
                else:
                    messagebox.showwarning(
                        "Recurso existente",
                        f"⚠️ El recurso '{nuevo}' ya existe",
                        parent=self.ventana
                    )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar: {e}", parent=self.ventana)
    
    def _cargar_eventos(self):
        """Carga los eventos existentes en la lista"""
        try:
            eventos = self.calendario.listar_eventos()
            
            if eventos:
                for i, evento in enumerate(eventos, 1):
                    # Mostrar recursos como texto
                    if evento.recursos:
                        recursos_texto = ", ".join(evento.recursos)
                    else:
                        recursos_texto = "Sin recursos"
                    
                    self.tree.insert("", "end", values=(
                        i,
                        evento.nombre,
                        evento.inicio,
                        evento.fin,
                        recursos_texto
                    ))
                
                self.contador_label.config(text=f"Eventos: {len(eventos)}")
        except Exception as e:
            print(f"Error cargando eventos: {e}")
            self.contador_label.config(text="Eventos: 0")
    
    def _agregar_evento(self):
        """Agrega un nuevo evento"""
        nombre = self.entry_nombre.get().strip()
        inicio = self.entry_inicio.get().strip()
        fin = self.entry_fin.get().strip()
        
        if nombre and inicio and fin:
            try:
                from modelos.evento import Evento
                from modelos.recurso import Recurso
                
                # Obtener recursos seleccionados
                recursos_seleccionados = list(self.lista_recursos_seleccionados.get(0, tk.END))
                
                # Crear evento
                evento = Evento(nombre, inicio, fin, recursos_seleccionados)
                
                # Marcar recursos como usados
                for recurso_nombre in recursos_seleccionados:
                    Recurso.marcar_como_usado(recurso_nombre, evento)
                
                self.calendario.agregar_evento(evento)
                
                # Actualizar tabla
                total_items = len(self.tree.get_children())
                self.tree.insert("", "end", values=(
                    total_items + 1,
                    nombre,
                    inicio,
                    fin,
                    ", ".join(recursos_seleccionados) if recursos_seleccionados else "Sin recursos"
                ))
                
                self.contador_label.config(text=f"Eventos: {total_items + 1}")
                self._limpiar_campos()
                self._actualizar_recursos_disponibles()
                
                messagebox.showinfo(
                    "Evento agregado",
                    f"✅ Evento '{nombre}' agregado\n"
                    f"Recursos asignados: {len(recursos_seleccionados)}",
                    parent=self.ventana
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo agregar el evento:\n{str(e)}",
                    parent=self.ventana
                )
        else:
            messagebox.showwarning(
                "Campos incompletos",
                "Debes ingresar nombre, inicio y fin.",
                parent=self.ventana
            )
    
    def _eliminar_evento(self):
        """Elimina el evento seleccionado"""
        seleccion = self.tree.selection()
        
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            nombre_evento = valores[1]
            
            respuesta = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar evento: {nombre_evento}?\n"
                f"Los recursos asignados serán liberados.",
                parent=self.ventana
            )
            
            if respuesta:
                # Buscar y liberar recursos
                try:
                    from modelos.recurso import Recurso
                    from modelos.evento import Evento
                    
                    # Obtener recursos del evento
                    recursos_texto = valores[4] if len(valores) > 4 else ""
                    if recursos_texto and recursos_texto != "Sin recursos":
                        recursos = [r.strip() for r in recursos_texto.split(',')]
                        # Crear objeto evento temporal para liberar
                        evento_temp = Evento(nombre_evento, "", "", [])
                        for recurso in recursos:
                            Recurso.liberar_recurso(recurso, evento_temp)
                    
                    # Actualizar disponibilidad
                    self._actualizar_recursos_disponibles()
                except Exception as e:
                    print(f"Error liberando recursos: {e}")
                
                # Eliminar de la tabla
                self.tree.delete(seleccion[0])
                total_actual = len(self.tree.get_children())
                self.contador_label.config(text=f"Eventos: {total_actual}")
                
                # Reindexar
                items = self.tree.get_children()
                for i, item_id in enumerate(items, 1):
                    valores_actuales = list(self.tree.item(item_id)['values'])
                    valores_actuales[0] = i
                    self.tree.item(item_id, values=valores_actuales)
        else:
            messagebox.showwarning(
                "Nada seleccionado",
                "Seleccione un evento para eliminar.",
                parent=self.ventana
            )
    
    def _actualizar_lista(self):
        """Actualiza la lista de eventos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self._cargar_eventos()
    
    def _limpiar_campos(self):
        """Limpia los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_inicio.delete(0, tk.END)
        self.entry_fin.delete(0, tk.END)
        self.lista_recursos_seleccionados.delete(0, tk.END)
        self._actualizar_recursos_disponibles()
    
    def _convocar_senado(self):
        """Convocar al senado"""
        messagebox.showinfo(
            "Senado",
            "El senado ha sido convocado. ¡Que comience el debate!",
            parent=self.ventana
        )
    
    def _volver_al_menu(self):
        """Vuelve al menú principal"""
        try:
            self.ventana.destroy()
        except:
            pass
        
        try:
            self.app.mostrar_menu()
        except Exception as e:
            print(f"Error al volver al menú: {e}")
            # Forzar cierre si hay error
            self.root.quit()
    
    def destruir(self):
        """Destruye la ventana"""
        try:
            self.ventana.destroy()
        except:
            pass