import sys
import os


# Configurar rutas
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR_ACTUAL)

# Directorio de datos
DIRECTORIO_DATOS = os.path.join(DIR_ACTUAL, "datos")
print(f"📁 Directorio de datos: {DIRECTORIO_DATOS}")

 # Importar la aplicación principal
from app import PlanificadorRomanoApp
    
print("\n" + "=" * 50)
print("🎮 INICIANDO APLICACIÓN...")
print("=" * 50)
    
# Crear y ejecutar la aplicación
app = PlanificadorRomanoApp()
app.iniciar()
    
