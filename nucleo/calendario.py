# nucleo/calendario.py - VERSIÓN COMPLETA
import os
import json
from modelos.evento import Evento
from nucleo.persistencia import Persistencia
from nucleo.buscador import Buscador

class Calendario:
    """Clase principal para gestionar el calendario imperial"""
    
    def __init__(self, directorio_datos="datos"):
        self.eventos = []
        self.directorio_datos = directorio_datos
        
        # Inicializar componentes
        self.persistencia = Persistencia(directorio_datos=directorio_datos)
        self.buscador = Buscador()
        
        # Cargar eventos al iniciar
        self.cargar_eventos()
    
    def agregar_evento(self, evento):
        """Agrega un evento al calendario"""
        # Validar que sea un Evento
        if not isinstance(evento, Evento):
            raise TypeError("Solo se pueden agregar objetos Evento")
            
        # Agregar evento
        self.eventos.append(evento)
        
        # Guardar automáticamente
        self.guardar_eventos()
        
        return True
    
    def eliminar_evento(self, nombre_evento):
        """Elimina un evento por nombre"""
        for i, evento in enumerate(self.eventos):
            if evento.nombre == nombre_evento:
                evento_eliminado = self.eventos.pop(i)
                self.guardar_eventos()  # Guardar cambios
                return evento_eliminado
        return None
    
    def obtener_evento(self, nombre_evento):
        """Obtiene un evento por nombre"""
        for evento in self.eventos:
            if evento.nombre == nombre_evento:
                return evento
        return None
    
    def listar_eventos(self):
        """Retorna una copia de la lista de eventos"""
        return self.eventos.copy()
    
    def guardar_eventos(self):
        """Guarda los eventos en archivo"""
        return self.persistencia.guardar_eventos(self.eventos)
    
    def cargar_eventos(self):
        """Carga eventos desde archivo"""
        eventos_cargados = self.persistencia.cargar_eventos()
        self.eventos = eventos_cargados
        return len(eventos_cargados)
    
    # MÉTODOS DE BÚSQUEDA (delegados al Buscador)
    
    def buscar_por_nombre(self, texto):
        """Busca eventos por nombre"""
        return self.buscador.buscar_por_nombre(self.eventos, texto)
    
    def buscar_por_recurso(self, recurso):
        """Busca eventos por recurso"""
        return self.buscador.buscar_por_recurso(self.eventos, recurso)
    
    def buscar_por_fecha(self, fecha):
        """Busca eventos por fecha"""
        return self.buscador.buscar_por_fecha(self.eventos, fecha)
    
    def buscar_por_rango_fechas(self, fecha_inicio, fecha_fin):
        """Busca eventos por rango de fechas"""
        return self.buscador.buscar_por_rango_fechas(self.eventos, fecha_inicio, fecha_fin)
    
    def ordenar_por_fecha(self, ascendente=True):
        """Ordena eventos por fecha"""
        return self.buscador.ordenar_por_fecha(self.eventos, ascendente)
    
    def ordenar_por_nombre(self, ascendente=True):
        """Ordena eventos por nombre"""
        return self.buscador.ordenar_por_nombre(self.eventos, ascendente)
    
    def eventos_proximos(self, dias=7):
        """Obtiene eventos próximos"""
        return self.buscador.eventos_proximos(self.eventos, dias)
    
    def eventos_en_curso(self):
        """Obtiene eventos en curso"""
        return self.buscador.eventos_en_curso(self.eventos)
    
    def eventos_pasados(self):
        """Obtiene eventos pasados"""
        return self.buscador.eventos_pasados(self.eventos)
    
    def eventos_sin_recursos(self):
        """Obtiene eventos sin recursos"""
        return self.buscador.buscar_eventos_sin_recursos(self.eventos)
    
    def estadisticas_recursos(self):
        """Obtiene estadísticas de recursos"""
        return self.buscador.estadisticas_recursos(self.eventos)
    
    def conteo_por_mes(self):
        """Obtiene conteo de eventos por mes"""
        return self.buscador.contar_eventos_por_mes(self.eventos)
    
    def generar_informe(self):
        """Genera un informe completo"""
        return self.buscador.generar_informe(self.eventos)
    
    def filtrar_por_recursos(self, min_recursos=0, max_recursos=None):
        """Filtra por cantidad de recursos"""
        return self.buscador.filtrar_por_cantidad_recursos(self.eventos, min_recursos, max_recursos)
    
    # MÉTODOS DE PERSISTENCIA AVANZADOS
    
    def exportar_datos(self, destino):
        """Exporta los datos a otra ubicación"""
        return self.persistencia.exportar_datos(destino)
    
    def importar_datos(self, origen, sobrescribir=True):
        """Importa datos desde otra ubicación"""
        return self.persistencia.importar_datos(origen, sobrescribir)
    
    def limpiar_datos(self):
        """Limpia todos los datos"""
        archivos_eliminados = self.persistencia.limpiar_datos()
        self.eventos = []  # Limpiar también en memoria
        return archivos_eliminados
    
    def obtener_estadisticas_datos(self):
        """Obtiene estadísticas de los archivos de datos"""
        return self.persistencia.obtener_estadisticas()
    
    def mostrar_eventos(self):
        """Muestra todos los eventos en consola (para debugging)"""
        if not self.eventos:
            print("📭 No hay eventos en el calendario")
            return
        
        print(f"📅 Calendario Imperial - {len(self.eventos)} eventos:")
        print("=" * 60)
        
        for i, evento in enumerate(self.eventos, 1):
            recursos_str = f", Recursos: {len(evento.recursos)}" if evento.recursos else ""
            print(f"{i:3d}. {evento.nombre} ({evento.inicio} - {evento.fin}{recursos_str})")
            if evento.recursos:
                print(f"     ⚔️  {', '.join(evento.recursos)}")