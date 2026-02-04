import sys 
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from datetime import datetime
from modelos.evento import Evento
from nucleo.calendario import Calendario

def test_conflicto_recursos():
    calendario = Calendario()
    e1 = Evento("Batalla",
                datetime(2025, 12, 7, 8, 0),
                datetime(2025, 12, 7, 12, 0),
                ["legion1", "centurion"])
    calendario.agregar_evento(e1)
    
    e2 = Evento("Otra batalla",
                datetime(2025, 12, 7, 9, 0),
                datetime(2025, 12, 7, 11, 0),
                ["legion1", "aguila"])
    
    try:
        calendario.agregar_evento(e2)
        print("test_conflicto_recursos: Fallo - daberia haber lanzado ValueError")
        return False
    except ValueError as e :
        if "Conflicto" in str(e):
            print("test_conflico_recursos: Paso")
            return True
        else:
            print(f"test_conflicto_recursos: Fallo - error incorrecto: {e}")
            return False
        
        
def test_sin_conflictos():
    calendario = Calendario()
    e1 = Evento("Batalla",
                datetime(2025, 12, 7, 12, 0),
                datetime(2025, 12, 7, 14, 0),
                ["legion1"])
    calendario.agregar_evento(e1)
    
    #Evento despues sin conflicos
    e2 = Evento("Desfile",
                datetime(2025, 12, 7, 12, 0),
                datetime(2025, 12, 7, 14, 0),
                ["legion1"])
    
    try:
        calendario.agregar_evento(e2)
        if len(calendario.eventos) == 2:
            print("test_sin_conflictos:PASO")
            return True
        else:
            print(f"test_sin_conflictos:FAllO - esperaba 2 eventos, tengo {len(calendario.eventos)}")
            return False
    except Exception as e:
        print("test_sin_conflictos: FALLO - error inesperado: {e}")
        return False
    
    
def test_diferentes_recursos():
    calendario = Calendario()
    e1 = Evento("Batalla",
                datetime(2025, 12, 7, 8, 0),
                datetime(2025, 12, 7, 12, 0),
                ["legion1"])
    calendario.agregar_evento(e1)
    
    #mismo horario pero recursos diferentes
    e2 = Evento("Consejo",
                datetime(2025, 12, 7, 9, 0),
                datetime(2025, 12, 7, 11, 0),
                ["senadores"])
    
    try:
        calendario.agregar_evento(e2)
        if len(calendario.eventos) == 2:
            print("test_diferentes_recursos: PASO")
            return True
        else:
            print(f"test_diferentes_recursos:FAllO - esperaba 2 eventos, tengo {len(calendario.eventos)}")
            return False
    except Exception as e:
        print("test_diferentes_recursos: FALLO - error inesperado: {e}")
        return False
    
        
def test_eventos_ordenados():
    """Prueba que los elementos se ordenan por fecha"""
    calendario = Calendario()
    
    #Agregar eventos en orden inverso
    e2 = Evento("Evento Tarde",
                datetime(2025, 12, 7, 15, 0),
                datetime(2025, 12, 7, 16, 0),
                ["legion1"])
    
    e1 = Evento("Evento Manana",
                datetime(2025, 12, 7, 8, 0),
                datetime(2025, 12, 7, 16, 0),
                ["Legion2"])
    calendario.agregar_evento(e2)
    calendario.agregar_evento(e1)
    
    
    eventos = calendario.listar_eventos()
    if eventos[0].nombre == "Evento Manana" and eventos[1].nombre == "Evento Tarde":
        print("test_eventos_ordenados: PASO")
        return True
    else:
        print("test_eventos_ordenados: FALLO - eventos no ordenados")
        print(f" Primer evento: {eventos[0].nombre}")
        print(f" Segundo evento: {eventos[1].nombre}")
        return False
    

def test_evento_sin_recursos():
    """Prueba evento sin recursos (lista vacia)"""
    calendario = Calendario()
    e1 = Evento("Reunion",
                datetime(2025, 12, 7, 8, 0),
                datetime(2025, 12, 7, 9, 0),
                [])

    try:
        calendario.agregar_evento(e1)
        if len(calendario.eventos) == 1 and calendario.eventos[0].recursos == []:
            print("test_evento_sin_recursos: PASO")
            return True
        else:
            print(f"test_evento_sin_recursos:FAllO")
            return False
    except Exception as e:
        print("test_evento_sin_recursos: FALLO - error: {e}")
        return False
    
def main():
    """Ejecuta todas las pruebas y muestra resultados"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DEL CALENDARIO ROMANO")
    print("="*60 + "\n")
    
    pruebas = [
        ("Conflicto de recursos", test_conflicto_recursos),
        ("Sin conflicto", test_sin_conflictos),
        ("Diferentes recursos", test_diferentes_recursos),
        ("Eventos orenados", test_eventos_ordenados)
        ("Evento sin recursos", test_evento_sin_recursos)
    ]
    
    resultados = []
    
    for nombre, prueba in pruebas:
        print(f"Ejecutando: {nombre}")
        try:
            resultado = prueba()
            resultados.append(resultado)
            print()
        except Exception as e:
            print(f"Error ejecutando {nombre}: {e}\n")
            resultados.append(False)
            
            
    print("="*60)
    print("RESUMEN DE PRUEBAS:")
    print("="*60)
    
    for i, (nombre, _) in enumerate(pruebas, 1):
        estado = "PASO" if resultados[i-1] else "FAllO"
        print(f"{i}.{nombre}: {estado}")
        
    exitos = sum(resultados)
    total = len(resultados)
    
    print(f"\n Resultado: {exitos}/{total} pruebas exitosas")
    
    if exitos == total:
        print("TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"{total -exitos} pruebas fallaron")
        
    print("="*60)
    
    return exitos == total

if __name__ == "__main__":
    
    archivos_necesarios = [
        ("evento.py", ROOT_DIR/ "evento.py"),
        ("núcleo/calendario.py", ROOT_DIR / "núcleo" / "calendario.py"),
    ]
    
    print("Verificando archivos necesarios...")
    for nombre, ruta in archivos_necesarios:
        if ruta.exists():
            print(f"{nombre}")
        else:
            print(f"{nombre} - NO ENCONTRADO")  
            print(f"Ruta: {ruta}")   
            
    main()
        