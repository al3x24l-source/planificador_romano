class Restricciones:
    def __init__(self):
        self.co_requisitos = []
        self.exclusiones = []
    
    def agregar_co_requisitos(self, recurso_a, recurso_b):
        """Si un evento usa recurso_a tambien debe usar recurso_b"""
        self.co_requisitos.append((recurso_a, recurso_b))
        
    
    def agregar_exclusiones(self, recurso_a, recurso_b):
        """recurso_a y recurso_b no pueden usarse en el mismo evento"""
        self.exclusiones.append((recurso_a, recurso_b))
    
    
    def validar(self, evento):
        # Validar co_requisitos
        for (a, b) in self.co_requisitos:
            if a in evento.recursos and b not in evento.recursos:
                raise ValueError(f"El recurso '{a}' requiere tambien el recurso '{b}'")
            
        # Validar exclusiones
        for (a, b) in self.exclusiones:
            if a in evento.recursos and b in evento.recursos:
                raise ValueError(f"El recurso '{a}' no puede usarse junto con '{b}'")
        
    