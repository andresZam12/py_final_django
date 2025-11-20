# 📋 Sistema de Control de Proyectos y Tareas

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![DRF](https://img.shields.io/badge/DRF-3.16.1-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

Sistema web para la gestión colaborativa de proyectos y seguimiento de tareas, desarrollado con Django y Django REST Framework.

## 🎯 Características Principales

- ✅ **Autenticación y Autorización**: Sistema completo de registro, login y roles (Admin/Miembro)
- 📊 **Dashboard Interactivo**: Estadísticas y gráficos en tiempo real
- 🎯 **Gestión de Proyectos**: CRUD completo con progreso visual
- ✔️ **Gestión de Tareas**: Asignación, prioridades y seguimiento de estado
- 💬 **Sistema de Comentarios**: Colaboración en tareas
- 📜 **Historial de Cambios**: Trazabilidad completa de modificaciones
- 🔔 **Notificaciones**: Alertas de asignaciones y vencimientos
- 📈 **Reportes**: Exportación a PDF y Excel
- 🚀 **API REST**: Endpoints completos con documentación Swagger

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.2.8**: Framework web principal
- **Django REST Framework 3.16.1**: API REST
- **Django Filter**: Filtrado avanzado
- **drf-spectacular**: Documentación automática de API
- **SimpleJWT**: Autenticación JWT

### Frontend
- **Bootstrap 5.3**: Framework CSS
- **Chart.js**: Gráficos interactivos
- **Font Awesome**: Iconos
- **jQuery**: Interactividad

### Base de Datos
- **SQLite**: Desarrollo
- **PostgreSQL**: Producción

### Reportes
- **ReportLab**: Generación de PDFs
- **openpyxl**: Exportación a Excel
- **Pandas**: Análisis de datos

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Virtualenv (recomendado)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/andresZam12/py_final_django.git
cd py_final_django
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias

```bash
cd CONTROL_PY_TAREAS
pip install -r requirements.txt
```

### 4. Configurar base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Colectar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 7. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
CONTROL_PY_TAREAS/
├── api/                    # API REST
│   ├── serializers.py      # Serializers de DRF
│   ├── views.py            # ViewSets
│   └── urls.py             # URLs de API
├── cuentas/                # Gestión de usuarios
│   ├── models.py           # Modelo User personalizado
│   ├── views.py            # Vistas de autenticación
│   └── forms.py            # Formularios de registro/login
├── proyectos/              # Gestión de proyectos y tareas
│   ├── models.py           # Modelos principales
│   ├── views.py            # Vistas CRUD
│   ├── forms.py            # Formularios
│   └── signals.py          # Signals para automatización
├── panel/                  # Dashboard
│   └── views.py            # Vista principal del dashboard
├── reportes/               # Generación de reportes
│   └── views.py            # Exportación PDF/Excel
├── templates/              # Plantillas HTML
│   ├── base.html           # Template base
│   ├── cuentas/            # Templates de autenticación
│   ├── proyectos/          # Templates de proyectos
│   └── panel/              # Templates del dashboard
├── static/                 # Archivos estáticos
│   ├── css/                # Estilos personalizados
│   ├── js/                 # JavaScript
│   └── img/                # Imágenes
└── manage.py               # Gestor de Django
```

## 🔑 Modelos Principales

### User (Personalizado)
- Roles: Admin / Miembro
- Campos adicionales para el sistema

### Proyecto
- Información del proyecto
- Relación con creador y miembros
- Cálculo automático de progreso

### Tarea
- Estados: Pendiente / En Progreso / Completada
- Prioridades: Baja / Media / Alta
- Asignación a usuarios
- Fechas límite

### Comentario
- Comentarios en tareas
- Historial de conversación

### Historial
- Registro automático de cambios
- Trazabilidad completa

### Notificación
- Alertas de asignaciones
- Avisos de vencimientos

## 🌐 API REST

### Endpoints Principales

```
GET    /api/proyectos/              # Listar proyectos
POST   /api/proyectos/              # Crear proyecto
GET    /api/proyectos/{id}/         # Detalle proyecto
PUT    /api/proyectos/{id}/         # Actualizar proyecto
DELETE /api/proyectos/{id}/         # Eliminar proyecto

GET    /api/tareas/                 # Listar tareas
POST   /api/tareas/                 # Crear tarea
GET    /api/tareas/mis_tareas/      # Mis tareas asignadas
GET    /api/tareas/proximas_vencer/ # Tareas próximas a vencer

GET    /api/notificaciones/         # Mis notificaciones
GET    /api/notificaciones/no_leidas/ # Notificaciones no leídas

POST   /api/token/                  # Obtener token JWT
POST   /api/token/refresh/          # Refrescar token
```

### Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema JSON**: `http://localhost:8000/api/schema/`

### Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

```bash
# Obtener token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"contraseña"}'

# Usar token en requests
curl -X GET http://localhost:8000/api/proyectos/ \
  -H "Authorization: Bearer {token}"
```

## 👥 Roles y Permisos

### Administrador
- Crear, editar y eliminar cualquier proyecto
- Gestionar usuarios
- Acceso completo al sistema
- Ver todas las estadísticas

### Miembro
- Crear proyectos propios
- Editar/eliminar solo proyectos creados por él
- Ver proyectos asignados
- Crear y gestionar tareas
- Comentar en tareas

## 📊 Dashboard

El dashboard incluye:

- 📈 Gráfico de tareas por estado
- 📊 Progreso de proyectos
- 👥 Top usuarios más activos
- ⏰ Tareas próximas a vencer
- 📋 Actividad reciente
- 📊 Estadísticas generales

## 📄 Reportes

### Reportes en PDF
- Resumen de proyecto con todas sus tareas
- Historial de cambios
- Estadísticas del proyecto

### Reportes en Excel
- Lista de tareas con filtros
- Exportación de proyectos
- Datos de miembros del equipo

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una app específica
python manage.py test proyectos

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Despliegue

### Configuración para Producción

1. Establecer `DEBUG = False` en settings.py
2. Configurar `ALLOWED_HOSTS`
3. Usar PostgreSQL en lugar de SQLite
4. Configurar variables de entorno con python-decouple
5. Usar Gunicorn como servidor WSGI
6. Configurar WhiteNoise para archivos estáticos

### Despliegue en Render

```bash
# Instalar dependencias de producción
pip install gunicorn psycopg2-binary whitenoise

# Crear archivo render.yaml
# Configurar variables de entorno en Render
# Deploy automático desde GitHub
```



## 📝 Licencia

Este proyecto fue desarrollado como proyecto final académico para la materia de Desarrollo Web con Django.

Desarrollado con ❤️ usando Django
