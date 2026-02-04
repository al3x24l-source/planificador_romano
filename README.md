PLANIFICADOR DE EVENTOS ROMANO

Sistema de gestión de eventos históricos con interfaz gráfica

🏛️ Descripción

Aplicación de escritorio desarrollada en Python para gestionar eventos con temática histórica. Permite crear, visualizar y administrar eventos a través de una interfaz gráfica inspirada en la antigua Roma.

📁 Estructura del Proyecto

```
planificador-romano/
├── main.py                    # Punto de entrada principal
├── app.py                     # Aplicación principal (controlador)
├── modelos/
│   └── evento.py             # Modelo de datos Evento
├── nucleo/
│   └── calendario.py         # Gestor de eventos
└── pantallas/
    ├── intro_epica.py        # Pantalla de introducción
    ├── menu_principal.py     # Menú de navegación
    └── gestion_eventos.py    # Gestión de eventos
```

🏗️ Componentes del Sistema

1. Modelos

· Evento: Representa un evento con nombre, fecha de inicio y fecha de fin
· Validaciones: Formato de fecha DD/MM/AAAA, rango temporal correcto
· Métodos: Cálculo de duración, conversión a diccionario

2. Núcleo

· Calendario: Gestor principal que almacena y administra eventos
· Funcionalidades: Agregar, listar y validar eventos
· Almacenamiento: Lista en memoria de objetos Evento

3. Pantallas

· Introducción Épica: Pantalla inicial con efectos visuales
· Menú Principal: Navegación entre secciones
· Gestión de Eventos: Interfaz completa para CRUD de eventos

4. Controlador

· PlanificadorRomanoApp: Coordina todos los componentes
· Navegación: Maneja transiciones entre pantallas
· Dependencias: Inyecta calendario a las pantallas

⚙️ Funcionalidades Implementadas

✅ Gestión Básica

· Crear nuevos eventos con nombre y fechas
· Listar todos los eventos en tabla organizada
· Eliminar eventos seleccionados
· Validar formato de fechas (DD/MM/AAAA)

✅ Interfaz de Usuario

· Formulario para ingreso de eventos
· Tabla con scroll para visualización
· Botones de acción intuitivos
· Mensajes de confirmación y error

✅ Validaciones

· Campos obligatorios completos
· Formato de fecha correcto
· Rango temporal válido (fin ≥ inicio)
· Confirmación para eliminaciones

🎮 Uso de la Aplicación

Ejecución

```bash
python main.py
```

Flujo de Uso

1. Introducción: Pantalla inicial con efectos visuales
2. Menú Principal: Seleccionar "Gestionar Eventos"
3. Formulario: Ingresar nombre, fecha inicio y fecha fin
4. Listado: Ver eventos en tabla organizada
5. Acciones: Agregar, eliminar o actualizar eventos

Formato de Fechas

· Entrada: DD/MM/AAAA (ej: 15/03/2024)
· Validación: Automática al agregar evento
· Cálculo: Duración automática en días

🎨 Interfaz Gráfica

Diseño Visual

· Tema romano con colores dorados y rojos oscuros
· Tipografías inspiradas en inscripciones romanas
· Botones con efectos hover
· Ventanas centradas automáticamente

Componentes Tkinter

· tk.Toplevel para ventanas secundarias
· ttk.Treeview para tabla de eventos
· tk.Entry para campos de formulario
· tk.Button para acciones del usuario
· tk.Label para textos y títulos

🔧 Requisitos Técnicos

Software

· Python 3.8 o superior
· Tkinter (incluido en Python estándar)

Estructura de Datos

```python
# Ejemplo de evento
evento = {
    "nombre": "Batalla de las Termópilas",
    "inicio": "01/08/2024",
    "fin": "03/08/2024"
}
```

📊 Características Técnicas

Arquitectura

· MVC: Separación Modelo-Vista-Controlador
· POO: Programación orientada a objetos
· Inyección de dependencias: Componentes desacoplados

Manejo de Errores

· Validación antes de operaciones críticas
· Mensajes de error descriptivos
· Recuperación ante excepciones

Navegación

· Flujo controlado entre pantallas
· Cierre apropiado de ventanas
· Retorno al menú principal

🚀 Ejecución Directa

1. Descargar todos los archivos del proyecto
2. Posicionarse en la carpeta principal
3. Ejecutar:

```bash
python main.py
```

📝 Formatos Aceptados

Evento Válido

```
Nombre: Sesión del Senado
Inicio: 15/03/2024
Fin: 15/03/2024
```

Evento Inválido

```
Nombre: (vacío)                    ❌ Error
Inicio: 2024-03-15                 ❌ Formato incorrecto
Fin: 14/03/2024                    ❌ Fecha anterior al inicio
```

👨‍💻 Desarrollo

Tecnologías

· Python: Lenguaje principal
· Tkinter: Interfaz gráfica
· JSON: (Planeado) Persistencia de datos

Metodología

· Desarrollo modular
· Código comentado
· Validaciones exhaustivas
· Manejo de errores robusto

---

¡Listo para organizar eventos históricos!