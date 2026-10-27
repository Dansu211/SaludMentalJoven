# Proyecto Web Colaborativo: Salud Mental Joven

Proyecto desarrollado para la asignatura de Ingeniería Web (Universidad de Deusto).

## 1. Estructura del Proyecto

```text
Proyectoweb/
├── appSaludMentalJoven/      # Aplicación Django (dominio y lógica)
│   ├── migrations/          # Historial de migraciones de la base de datos
│   ├── static/              # Archivos estáticos
│   │   └── css/
│   │       └── style.css
│   ├── templates/           # Plantillas HTML directas (base.html, index.html, etc.)
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   ├── admin.py             # Registro de modelos en el administrador de Django
│   ├── apps.py              # Configuración de la aplicación
│   ├── models.py            # Modelos y entidades de datos
│   ├── tests.py             # Pruebas unitarias
│   ├── urls.py              # Rutas de la aplicación
│   └── views.py             # Lógica de las vistas
├── saludMentalJoven/        # Paquete de configuración global del proyecto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configuración principal (apps, idioma, base de datos)
│   ├── urls.py              # Enrutador principal del proyecto
│   └── wsgi.py
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Exclusión de ficheros temporales y entornos
├── db.sqlite3               # Base de datos SQLite local
├── manage.py                # Utilidad de línea de comandos de Django
└── README.md                # Documentación del proyecto
```

## 2. Requisitos Previos

- Python 3.11 o superior.
- Entorno virtual (`venv`).

## 3. Puesta en Marcha

1. **Activar el entorno virtual** (en Windows PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

4. **Crear un superusuario** (para acceder al panel de administración):
   ```bash
   python manage.py createsuperuser
   ```

5. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```
   Acceso a la web: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
   Acceso a administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 4. Estado Actual

- Estructura adaptada al patrón de las prácticas de clase (`app<Nombre>` y `<Nombre>` para el proyecto).
- Plantillas ubicadas directamente en `templates/` (`base.html`, `index.html`) con herencia limpia.
- Estilos CSS3 organizados en `static/css/` compatibles con validadores W3C.
- Pendiente: definir modelos según el enunciado oficial y registrarlos en `admin.py`.
