# modelos/evento.py
class Evento:
    """Clase que representa un evento en el calendario romano"""
    
    def __init__(self, nombre, inicio, fin, recursos=None):
        """
        Inicializa un nuevo evento
        
        Args:
            nombre (str): Nombre del evento
            inicio (str): Fecha de inicio (DD/MM/AAAA)
            fin (str): Fecha de fin (DD/MM/AAAA)
            recursos (list): Lista de recursos asignados (opcional)
        """
        self.nombre = nombre
        self.inicio = inicio
        self.fin = fin
        self.recursos = recursos if recursos else []
    
    def __str__(self):
        """Representación en string del evento"""
        recursos_str = f", Recursos: {len(self.recursos)}" if self.recursos else ""
        return f"{self.nombre} ({self.inicio} - {self.fin}{recursos_str})"
    
    def agregar_recurso(self, recurso):
        """Agrega un recurso al evento"""
        if recurso not in self.recursos:
            self.recursos.append(recurso)
            return True
        return False
    
    def quitar_recurso(self, recurso):
        """Quita un recurso del evento"""
        if recurso in self.recursos:
            self.recursos.remove(recurso)
            return True
        return False
    
    def tiene_recursos(self):
        """Verifica si el evento tiene recursos asignados"""
        return len(self.recursos) > 0# modelos/evento.py
