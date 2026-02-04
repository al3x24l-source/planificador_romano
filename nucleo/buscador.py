# nucleo/buscador.py
from datetime import datetime

class Buscador:
    """Clase para buscar y filtrar eventos en el calendario imperial"""
    
    @staticmethod
    def buscar_por_nombre(eventos, texto_busqueda):
        """Busca eventos que contengan el texto en el nombre"""
        if not texto_busqueda:
            return eventos
        
        texto_busqueda = texto_busqueda.lower()
        resultados = []
        
        for evento in eventos:
            if texto_busqueda in evento.nombre.lower():
                resultados.append(evento)
        
        return resultados
    
    @staticmethod
    def buscar_por_recurso(eventos, nombre_recurso):
        """Busca eventos que usen un recurso específico"""
        if not nombre_recurso:
            return eventos
        
        nombre_recurso = nombre_recurso.lower()
        resultados = []
        
        for evento in eventos:
            for recurso in evento.recursos:
                if nombre_recurso in recurso.lower():
                    resultados.append(evento)
                    break  # Solo agregar una vez
        
        return resultados
    
    @staticmethod
    def buscar_por_fecha(eventos, fecha):
        """Busca eventos que ocurran en una fecha específica"""
        if not fecha:
            return eventos
        
        try:
            fecha_busqueda = datetime.strptime(fecha, "%d/%m/%Y")
            resultados = []
            
            for evento in eventos:
                try:
                    evento_inicio = datetime.strptime(evento.inicio, "%d/%m/%Y")
                    evento_fin = datetime.strptime(evento.fin, "%d/%m/%Y")
                    
                    if evento_inicio <= fecha_busqueda <= evento_fin:
                        resultados.append(evento)
                        
                except ValueError:
                    continue  # Si hay error en formato de fecha, saltar este evento
            
            return resultados
            
        except ValueError:
            print("⚠️ Formato de fecha incorrecto. Use DD/MM/AAAA")
            return []
    
    @staticmethod
    def buscar_por_rango_fechas(eventos, fecha_inicio, fecha_fin):
        """Busca eventos dentro de un rango de fechas"""
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
            
            resultados = []
            
            for evento in eventos:
                try:
                    evento_inicio = datetime.strptime(evento.inicio, "%d/%m/%Y")
                    evento_fin = datetime.strptime(evento.fin, "%d/%m/%Y")
                    
                    # Verificar si hay superposición de fechas
                    if (evento_inicio <= fecha_fin_dt and evento_fin >= fecha_inicio_dt):
                        resultados.append(evento)
                        
                except ValueError:
                    continue
            
            return resultados
            
        except ValueError:
            print("⚠️ Formato de fecha incorrecto. Use DD/MM/AAAA")
            return []
    
    @staticmethod
    def ordenar_por_fecha(eventos, ascendente=True):
        """Ordena eventos por fecha de inicio"""
        eventos_ordenados = eventos.copy()
        
        def obtener_fecha(evento):
            try:
                return datetime.strptime(evento.inicio, "%d/%m/%Y")
            except ValueError:
                return datetime.min  # Fecha muy antigua para errores
        
        eventos_ordenados.sort(key=obtener_fecha, reverse=not ascendente)
        return eventos_ordenados
    
    @staticmethod
    def ordenar_por_nombre(eventos, ascendente=True):
        """Ordena eventos por nombre"""
        eventos_ordenados = eventos.copy()
        eventos_ordenados.sort(key=lambda e: e.nombre.lower(), reverse=not ascendente)
        return eventos_ordenados
    
    @staticmethod
    def eventos_proximos(eventos, dias=7):
        """Encuentra eventos que comienzan en los próximos N días"""
        resultados = []
        hoy = datetime.now()
        
        for evento in eventos:
            try:
                evento_inicio = datetime.strptime(evento.inicio, "%d/%m/%Y")
                diferencia = (evento_inicio - hoy).days
                
                if 0 <= diferencia <= dias:
                    resultados.append((evento, diferencia))
                    
            except ValueError:
                continue
        
        # Ordenar por proximidad
        resultados.sort(key=lambda x: x[1])
        return [evento for evento, _ in resultados]
    
    @staticmethod
    def eventos_pasados(eventos):
        """Encuentra eventos que ya han terminado"""
        resultados = []
        hoy = datetime.now()
        
        for evento in eventos:
            try:
                evento_fin = datetime.strptime(evento.fin, "%d/%m/%Y")
                
                if evento_fin < hoy:
                    resultados.append(evento)
                    
            except ValueError:
                continue
        
        return resultados
    
    @staticmethod
    def eventos_en_curso(eventos):
        """Encuentra eventos que están en curso actualmente"""
        resultados = []
        hoy = datetime.now()
        
        for evento in eventos:
            try:
                evento_inicio = datetime.strptime(evento.inicio, "%d/%m/%Y")
                evento_fin = datetime.strptime(evento.fin, "%d/%m/%Y")
                
                if evento_inicio <= hoy <= evento_fin:
                    resultados.append(evento)
                    
            except ValueError:
                continue
        
        return resultados
    
    @staticmethod
    def contar_eventos_por_mes(eventos):
        """Cuenta cuántos eventos hay por mes"""
        conteo = {}
        
        for evento in eventos:
            try:
                evento_inicio = datetime.strptime(evento.inicio, "%d/%m/%Y")
                mes_key = f"{evento_inicio.year}-{evento_inicio.month:02d}"
                
                if mes_key in conteo:
                    conteo[mes_key] += 1
                else:
                    conteo[mes_key] = 1
                    
            except ValueError:
                continue
        
        return conteo
    
    @staticmethod
    def estadisticas_recursos(eventos):
        """Genera estadísticas de uso de recursos"""
        estadisticas = {}
        
        for evento in eventos:
            for recurso in evento.recursos:
                if recurso in estadisticas:
                    estadisticas[recurso] += 1
                else:
                    estadisticas[recurso] = 1
        
        # Ordenar por frecuencia de uso
        return dict(sorted(estadisticas.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def filtrar_por_cantidad_recursos(eventos, min_recursos=0, max_recursos=None):
        """Filtra eventos por cantidad de recursos asignados"""
        resultados = []
        
        for evento in eventos:
            cantidad = len(evento.recursos)
            
            if cantidad >= min_recursos:
                if max_recursos is None or cantidad <= max_recursos:
                    resultados.append(evento)
        
        return resultados
    
    @staticmethod
    def buscar_eventos_sin_recursos(eventos):
        """Encuentra eventos que no tienen recursos asignados"""
        return [evento for evento in eventos if len(evento.recursos) == 0]
    
    @staticmethod
    def generar_informe(eventos):
        """Genera un informe completo de todos los eventos"""
        informe = {
            'total_eventos': len(eventos),
            'eventos_proximos_7_dias': len(Buscador.eventos_proximos(eventos, 7)),
            'eventos_en_curso': len(Buscador.eventos_en_curso(eventos)),
            'eventos_pasados': len(Buscador.eventos_pasados(eventos)),
            'eventos_sin_recursos': len(Buscador.buscar_eventos_sin_recursos(eventos)),
            'estadisticas_recursos': Buscador.estadisticas_recursos(eventos),
            'conteo_por_mes': Buscador.contar_eventos_por_mes(eventos)
        }
        
        return informe