# nucleo/persistencia.py
import json
import os
from modelos.evento import Evento

class Persistencia:
    """Clase para manejar la persistencia de datos del Planificador Imperial"""
    
    def __init__(self, directorio_datos="datos"):
        self.directorio_datos = directorio_datos
        self._crear_directorio_si_no_existe()
    
    def _crear_directorio_si_no_existe(self):
        """Crea el directorio de datos si no existe"""
        if not os.path.exists(self.directorio_datos):
            os.makedirs(self.directorio_datos)
            print(f"📁 Directorio '{self.directorio_datos}' creado")
    
    def guardar_eventos(self, eventos, nombre_archivo="eventos.json"):
        """Guarda la lista de eventos en un archivo JSON"""
        try:
            ruta_archivo = os.path.join(self.directorio_datos, nombre_archivo)
            
            # Convertir eventos a diccionarios
            eventos_dict = []
            for evento in eventos:
                evento_dict = {
                    'nombre': evento.nombre,
                    'inicio': evento.inicio,
                    'fin': evento.fin,
                    'recursos': evento.recursos
                }
                eventos_dict.append(evento_dict)
            
            # Guardar en archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(eventos_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Eventos guardados en {ruta_archivo}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando eventos: {e}")
            return False
    
    def cargar_eventos(self, nombre_archivo="eventos.json"):
        """Carga eventos desde un archivo JSON"""
        try:
            ruta_archivo = os.path.join(self.directorio_datos, nombre_archivo)
            
            if not os.path.exists(ruta_archivo):
                print(f"ℹ️ No existe archivo {ruta_archivo}, se creará uno nuevo")
                return []
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                eventos_dict = json.load(f)
            
            # Convertir diccionarios a objetos Evento
            eventos = []
            for evento_dict in eventos_dict:
                evento = Evento(
                    nombre=evento_dict['nombre'],
                    inicio=evento_dict['inicio'],
                    fin=evento_dict['fin'],
                    recursos=evento_dict.get('recursos', [])
                )
                eventos.append(evento)
            
            print(f"✅ {len(eventos)} eventos cargados desde {ruta_archivo}")
            return eventos
            
        except json.JSONDecodeError:
            print(f"⚠️ Archivo corrupto o vacío, se iniciará con lista vacía")
            return []
        except Exception as e:
            print(f"❌ Error cargando eventos: {e}")
            return []
    
    def guardar_recursos(self, recursos_disponibles, recursos_usados, nombre_archivo="recursos.json"):
        """Guarda el estado de los recursos en un archivo JSON"""
        try:
            ruta_archivo = os.path.join(self.directorio_datos, nombre_archivo)
            
            recursos_data = {
                'disponibles': recursos_disponibles,
                'usados': recursos_usados
            }
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(recursos_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Recursos guardados en {ruta_archivo}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando recursos: {e}")
            return False
    
    def cargar_recursos(self, nombre_archivo="recursos.json"):
        """Carga el estado de los recursos desde un archivo JSON"""
        try:
            ruta_archivo = os.path.join(self.directorio_datos, nombre_archivo)
            
            if not os.path.exists(ruta_archivo):
                print(f"ℹ️ No existe archivo {ruta_archivo}, se usará estado inicial")
                return [], {}
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                recursos_data = json.load(f)
            
            disponibles = recursos_data.get('disponibles', [])
            usados = recursos_data.get('usados', {})
            
            print(f"✅ Recursos cargados desde {ruta_archivo}")
            return disponibles, usados
            
        except json.JSONDecodeError:
            print(f"⚠️ Archivo corrupto o vacío, se iniciará con estado inicial")
            return [], {}
        except Exception as e:
            print(f"❌ Error cargando recursos: {e}")
            return [], {}
    
    def exportar_datos(self, destino, incluir_eventos=True, incluir_recursos=True):
        """Exporta los datos a otra ubicación"""
        try:
            if not os.path.exists(destino):
                os.makedirs(destino)
            
            archivos_exportados = []
            
            if incluir_eventos:
                origen_eventos = os.path.join(self.directorio_datos, "eventos.json")
                destino_eventos = os.path.join(destino, "eventos.json")
                if os.path.exists(origen_eventos):
                    import shutil
                    shutil.copy2(origen_eventos, destino_eventos)
                    archivos_exportados.append("eventos.json")
            
            if incluir_recursos:
                origen_recursos = os.path.join(self.directorio_datos, "recursos.json")
                destino_recursos = os.path.join(destino, "recursos.json")
                if os.path.exists(origen_recursos):
                    import shutil
                    shutil.copy2(origen_recursos, destino_recursos)
                    archivos_exportados.append("recursos.json")
            
            print(f"✅ Datos exportados a {destino}: {', '.join(archivos_exportados)}")
            return archivos_exportados
            
        except Exception as e:
            print(f"❌ Error exportando datos: {e}")
            return []
    
    def importar_datos(self, origen, sobrescribir=True):
        """Importa datos desde otra ubicación"""
        try:
            archivos_importados = []
            
            origen_eventos = os.path.join(origen, "eventos.json")
            destino_eventos = os.path.join(self.directorio_datos, "eventos.json")
            
            if os.path.exists(origen_eventos):
                import shutil
                shutil.copy2(origen_eventos, destino_eventos)
                archivos_importados.append("eventos.json")
            
            origen_recursos = os.path.join(origen, "recursos.json")
            destino_recursos = os.path.join(self.directorio_datos, "recursos.json")
            
            if os.path.exists(origen_recursos):
                import shutil
                shutil.copy2(origen_recursos, destino_recursos)
                archivos_importados.append("recursos.json")
            
            print(f"✅ Datos importados desde {origen}: {', '.join(archivos_importados)}")
            return archivos_importados
            
        except Exception as e:
            print(f"❌ Error importando datos: {e}")
            return []
    
    def limpiar_datos(self):
        """Limpia todos los datos guardados"""
        try:
            archivos_eliminados = 0
            
            eventos_path = os.path.join(self.directorio_datos, "eventos.json")
            if os.path.exists(eventos_path):
                os.remove(eventos_path)
                archivos_eliminados += 1
                print(f"🗑️ Archivo eventos.json eliminado")
            
            recursos_path = os.path.join(self.directorio_datos, "recursos.json")
            if os.path.exists(recursos_path):
                os.remove(recursos_path)
                archivos_eliminados += 1
                print(f"🗑️ Archivo recursos.json eliminado")
            
            return archivos_eliminados
            
        except Exception as e:
            print(f"❌ Error limpiando datos: {e}")
            return 0
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de los archivos de datos"""
        try:
            estadisticas = {
                'directorio': self.directorio_datos,
                'existe': os.path.exists(self.directorio_datos),
                'archivos': []
            }
            
            if estadisticas['existe']:
                for archivo in os.listdir(self.directorio_datos):
                    ruta_archivo = os.path.join(self.directorio_datos, archivo)
                    if os.path.isfile(ruta_archivo):
                        tamaño = os.path.getsize(ruta_archivo)
                        estadisticas['archivos'].append({
                            'nombre': archivo,
                            'tamaño_bytes': tamaño,
                            'tamaño_kb': tamaño / 1024
                        })
            
            return estadisticas
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
        

