# Proyecto Web Colaborativo: Salud Mental Joven

Proyecto desarrollado para la asignatura de Ingeniería Web (Universidad de Deusto).

Este repositorio corresponde a la entrega **E4a**: el proyecto Django con las funcionalidades añadidas.

## 1. Estructura del Proyecto

```text
SaludMentalJoven/
├── appSaludMentalJoven/       # Aplicación Django (dominio y lógica)
│   ├── fixtures/
│   │   └── datos_iniciales.json   # Datos iniciales de todas las entidades (E4a opción 5)
│   ├── migrations/            # Historial de migraciones de la base de datos
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js         # Interacción en el cliente y AJAX (E4a opción 1)
│   ├── templates/             # Plantillas HTML (base.html + una por página)
│   ├── admin.py               # Registro de modelos en el administrador
│   ├── forms.py               # Formulario de inscripción, un ModelForm (E4a opción 3)
│   ├── models.py              # Modelos y relaciones
│   ├── tests.py               # Pruebas
│   ├── urls.py                # Rutas de la aplicación
│   └── views.py               # Vistas basadas en clases (E4a opción 2)
├── locale/en/LC_MESSAGES/     # Traducciones al inglés .po/.mo (E4a opción 6)
├── saludMentalJoven/          # Configuración global (settings, urls raíz con i18n)
├── requirements.txt
├── db.sqlite3
└── manage.py
```

## 2. Requisitos Previos

- Python 3.11 o superior y un entorno virtual (`venv`).

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

4. **Cargar los datos iniciales** (solo hace falta con una base de datos vacía):
   ```bash
   python manage.py loaddata datos_iniciales
   ```

5. **Crear un superusuario** (para acceder al panel de administración):
   ```bash
   python manage.py createsuperuser

   Superusuario de prueba:
   username-->admin
   password-->admin123
   ```

6. **Iniciar el servidor de desarrollo Django**:
   ```bash
   python manage.py runserver

   .\venv\Scripts\python.exe manage.py runserver
   ```
   Acceso a la web: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (redirige a `/es/`)  
   Versión en inglés: [http://127.0.0.1:8000/en/](http://127.0.0.1:8000/en/)  
   Acceso a administración: [http://127.0.0.1:8000/es/admin/](http://127.0.0.1:8000/es/admin/)

7. **Ejecutar las pruebas**:
   ```bash
   python manage.py test appSaludMentalJoven
   ```

## 4. Funcionalidades añadidas (E4a)

| Opción | Puntos | Qué se ha hecho |
|---|---|---|
| 1. JavaScript / AJAX | 0,50 | `static/js/main.js`: buscador de artículos por AJAX (JSON), inscripción en actividades por AJAX sin recargar la página, filtro de recursos por formato con animación y botón «volver arriba». |
| 2. Vistas basadas en clases | 0,50 | Todas las vistas usan `TemplateView`, `ListView`, `DetailView` o `View`. |
| 3. Formularios | 0,50 | Nueva entidad `Inscripcion` y `InscripcionForm` (`ModelForm`) en el detalle de cada actividad. |
| 5. Datos iniciales | 0,25 | `fixtures/datos_iniciales.json` con todas las entidades. |
| 6. Multilingüismo (i18n) | 0,50 | Español e inglés, URLs con prefijo `/es/` y `/en/` y selector de idioma. |
