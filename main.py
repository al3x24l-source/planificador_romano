# main.py - PUNTO DE ENTRADA PRINCIPAL
import sys
import os

print("⚔️ PLANIFICADOR IMPERIAL ROMANO ⚔️")
print("=" * 50)

# Configurar rutas
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR_ACTUAL)

# Directorio de datos
DIRECTORIO_DATOS = os.path.join(DIR_ACTUAL, "datos")
print(f"📁 Directorio de datos: {DIRECTORIO_DATOS}")

try:
    # Importar la aplicación principal
    from app import PlanificadorRomanoApp
    
    print("\n" + "=" * 50)
    print("🎮 INICIANDO APLICACIÓN...")
    print("=" * 50)
    
    # Crear y ejecutar la aplicación
    app = PlanificadorRomanoApp()
    app.iniciar()
    
except ImportError as e:
    print(f"\n❌ ERROR CRÍTICO: No se pudo cargar la aplicación")
    print(f"   Detalles: {e}")
    print("\n🔧 Verifica que todos los archivos estén en su lugar:")
    print("   - app.py")
    print("   - modelos/")
    print("   - nucleo/")
    print("   - pantallas/")
    
    input("\nPresiona Enter para salir...")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()
    input("\nPresiona Enter para salir...")
    sys.exit(1)