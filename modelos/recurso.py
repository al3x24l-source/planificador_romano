# modelos/recurso.py
import os
import json

class Recurso:
    """Clase para gestionar recursos con disponibilidad"""
    
    recursos_disponibles = []  # Lista global de recursos disponibles
    recursos_usados = {}  # Diccionario: {nombre_recurso: [eventos_que_lo_usaron]}
    
    @classmethod
    def inicializar(cls, directorio_datos="datos"):
        """Inicializa recursos desde archivo"""
        archivo_recursos = os.path.join(directorio_datos, "recursos.json")
        
        # Asegurar que el directorio existe
        if not os.path.exists(directorio_datos):
            os.makedirs(directorio_datos)
            print(f"📁 Directorio '{directorio_datos}' creado")
        
        # Cargar recursos si el archivo existe
        if os.path.exists(archivo_recursos):
            try:
                with open(archivo_recursos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                cls.recursos_disponibles = datos.get('disponibles', [])
                cls.recursos_usados = datos.get('usados', {})
                print(f"✅ Recursos cargados desde {archivo_recursos}")
            except Exception as e:
                print(f"⚠️ Error cargando recursos: {e}")
                cls.recursos_disponibles = []
                cls.recursos_usados = {}
        else:
            print(f"ℹ️ No existe archivo {archivo_recursos}, se usará lista vacía")
            cls.recursos_disponibles = []
            cls.recursos_usados = {}
    
    @classmethod
    def guardar_estado(cls, directorio_datos="datos"):
        """Guarda el estado actual de los recursos"""
        try:
            archivo_recursos = os.path.join(directorio_datos, "recursos.json")
            
            datos = {
                'disponibles': cls.recursos_disponibles,
                'usados': cls.recursos_usados
            }
            
            with open(archivo_recursos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error guardando recursos: {e}")
            return False
    
    @classmethod
    def obtener_disponibles(cls):
        """Retorna recursos no utilizados"""
        disponibles = []
        for recurso in cls.recursos_disponibles:
            if len(cls.recursos_usados.get(recurso, [])) == 0:
                disponibles.append(recurso)
        return disponibles
    
    @classmethod
    def obtener_todos(cls):
        """Retorna todos los recursos registrados"""
        return cls.recursos_disponibles.copy()
    
    @classmethod
    def agregar_recurso(cls, nombre):
        """Agrega un nuevo recurso al sistema"""
        if nombre not in cls.recursos_disponibles:
            cls.recursos_disponibles.append(nombre)
            cls.recursos_usados[nombre] = []
            cls.guardar_estado()  # Guardar automáticamente
            return True
        return False
    
    @classmethod
    def marcar_como_usado(cls, nombre_recurso, evento):
        """Marca un recurso como usado por un evento"""
        if nombre_recurso in cls.recursos_usados:
            if evento.nombre not in cls.recursos_usados[nombre_recurso]:
                cls.recursos_usados[nombre_recurso].append(evento.nombre)
                cls.guardar_estado()  # Guardar automáticamente
    
    @classmethod
    def liberar_recurso(cls, nombre_recurso, evento):
        """Libera un recurso usado por un evento"""
        if nombre_recurso in cls.recursos_usados:
            if evento.nombre in cls.recursos_usados[nombre_recurso]:
                cls.recursos_usados[nombre_recurso].remove(evento.nombre)
                cls.guardar_estado()  # Guardar automáticamente
    
    @classmethod
    def esta_disponible(cls, nombre_recurso):
        """Verifica si un recurso está disponible"""
        if nombre_recurso in cls.recursos_usados:
            return len(cls.recursos_usados[nombre_recurso]) == 0
        return False
    
    def __str__(self):
        return self.nombre