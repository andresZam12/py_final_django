# Script para crear datos de prueba
# Ejecutar con: python manage.py shell < crear_datos_prueba.py

from django.contrib.auth import get_user_model
from proyectos.models import Proyecto, Tarea, Comentario
from datetime import date, timedelta
from django.utils import timezone

User = get_user_model()

print("🚀 Creando datos de prueba...")

# Crear usuarios
print("\n👥 Creando usuarios...")
try:
    # Usuario admin (si no existe)
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@ejemplo.com',
            password='admin123',
            role='admin',
            first_name='Administrador',
            last_name='Sistema'
        )
        print(f"✅ Superusuario creado: {admin.username}")
    else:
        admin = User.objects.get(username='admin')
        print(f"ℹ️  Superusuario ya existe: {admin.username}")

    # Usuarios regulares
    users_data = [
        {'username': 'andres', 'email': 'andres@ejemplo.com', 'first_name': 'Andrés', 'last_name': 'González', 'role': 'admin'},
        {'username': 'maria', 'email': 'maria@ejemplo.com', 'first_name': 'María', 'last_name': 'López', 'role': 'member'},
        {'username': 'carlos', 'email': 'carlos@ejemplo.com', 'first_name': 'Carlos', 'last_name': 'Ramírez', 'role': 'member'},
        {'username': 'laura', 'email': 'laura@ejemplo.com', 'first_name': 'Laura', 'last_name': 'Martínez', 'role': 'member'},
    ]

    usuarios = []
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            usuarios.append(user)
            print(f"✅ Usuario creado: {user.username}")
        else:
            user = User.objects.get(username=user_data['username'])
            usuarios.append(user)
            print(f"ℹ️  Usuario ya existe: {user.username}")

except Exception as e:
    print(f"❌ Error creando usuarios: {e}")
    exit(1)

# Crear proyectos
print("\n📁 Creando proyectos...")
proyectos_data = [
    {
        'nombre': 'Sistema de Gestión Empresarial',
        'descripcion': 'Desarrollo de un sistema completo de gestión empresarial con módulos de inventario, ventas y reportes.',
        'creado_por': usuarios[0],
        'fecha_inicio': date.today() - timedelta(days=30),
        'fecha_fin': date.today() + timedelta(days=60),
    },
    {
        'nombre': 'Aplicación Móvil E-Commerce',
        'descripcion': 'App móvil para comercio electrónico con integración de pagos y notificaciones push.',
        'creado_por': usuarios[1],
        'fecha_inicio': date.today() - timedelta(days=15),
        'fecha_fin': date.today() + timedelta(days=45),
    },
    {
        'nombre': 'Portal Web Corporativo',
        'descripcion': 'Sitio web institucional con sistema de noticias, galería y formularios de contacto.',
        'creado_por': usuarios[0],
        'fecha_inicio': date.today(),
        'fecha_fin': date.today() + timedelta(days=30),
    },
]

proyectos = []
for proyecto_data in proyectos_data:
    if not Proyecto.objects.filter(nombre=proyecto_data['nombre']).exists():
        proyecto = Proyecto.objects.create(**proyecto_data)
        proyectos.append(proyecto)
        print(f"✅ Proyecto creado: {proyecto.nombre}")
    else:
        proyecto = Proyecto.objects.get(nombre=proyecto_data['nombre'])
        proyectos.append(proyecto)
        print(f"ℹ️  Proyecto ya existe: {proyecto.nombre}")

# Crear tareas
print("\n📝 Creando tareas...")
tareas_data = [
    # Proyecto 1
    {
        'titulo': 'Diseñar base de datos',
        'descripcion': 'Crear el modelo de datos y las relaciones entre tablas',
        'proyecto': proyectos[0],
        'asignado_a': usuarios[2],
        'prioridad': 'alta',
        'estado': 'completada',
        'fecha_vencimiento': date.today() - timedelta(days=5),
    },
    {
        'titulo': 'Implementar API REST',
        'descripcion': 'Desarrollar endpoints de la API con Django REST Framework',
        'proyecto': proyectos[0],
        'asignado_a': usuarios[0],
        'prioridad': 'alta',
        'estado': 'en_progreso',
        'fecha_vencimiento': date.today() + timedelta(days=7),
    },
    {
        'titulo': 'Crear dashboard administrativo',
        'descripcion': 'Interface de administración con gráficas y estadísticas',
        'proyecto': proyectos[0],
        'asignado_a': usuarios[1],
        'prioridad': 'media',
        'estado': 'pendiente',
        'fecha_vencimiento': date.today() + timedelta(days=14),
    },
    {
        'titulo': 'Implementar módulo de reportes',
        'descripcion': 'Sistema de generación de reportes en PDF y Excel',
        'proyecto': proyectos[0],
        'asignado_a': usuarios[2],
        'prioridad': 'media',
        'estado': 'pendiente',
        'fecha_vencimiento': date.today() + timedelta(days=21),
    },
    
    # Proyecto 2
    {
        'titulo': 'Diseño UI/UX de la app',
        'descripcion': 'Crear mockups y prototipos de todas las pantallas',
        'proyecto': proyectos[1],
        'asignado_a': usuarios[1],
        'prioridad': 'alta',
        'estado': 'completada',
        'fecha_vencimiento': date.today() - timedelta(days=3),
    },
    {
        'titulo': 'Integrar pasarela de pagos',
        'descripcion': 'Implementar Stripe/PayPal para procesamiento de pagos',
        'proyecto': proyectos[1],
        'asignado_a': usuarios[0],
        'prioridad': 'alta',
        'estado': 'en_progreso',
        'fecha_vencimiento': date.today() + timedelta(days=10),
    },
    {
        'titulo': 'Sistema de notificaciones push',
        'descripcion': 'Configurar Firebase Cloud Messaging',
        'proyecto': proyectos[1],
        'asignado_a': usuarios[3],
        'prioridad': 'media',
        'estado': 'pendiente',
        'fecha_vencimiento': date.today() + timedelta(days=15),
    },
    
    # Proyecto 3
    {
        'titulo': 'Configurar hosting y dominio',
        'descripcion': 'Contratar hosting y configurar dominio DNS',
        'proyecto': proyectos[2],
        'asignado_a': usuarios[2],
        'prioridad': 'alta',
        'estado': 'en_progreso',
        'fecha_vencimiento': date.today() + timedelta(days=5),
    },
    {
        'titulo': 'Desarrollar sistema de noticias',
        'descripcion': 'CRUD de noticias con editor de texto enriquecido',
        'proyecto': proyectos[2],
        'asignado_a': usuarios[1],
        'prioridad': 'baja',
        'estado': 'pendiente',
        'fecha_vencimiento': date.today() + timedelta(days=20),
    },
    {
        'titulo': 'Optimizar SEO',
        'descripcion': 'Implementar meta tags, sitemap y optimización para buscadores',
        'proyecto': proyectos[2],
        'asignado_a': usuarios[3],
        'prioridad': 'baja',
        'estado': 'pendiente',
        'fecha_vencimiento': date.today() + timedelta(days=25),
    },
]

tareas = []
for tarea_data in tareas_data:
    if not Tarea.objects.filter(titulo=tarea_data['titulo'], proyecto=tarea_data['proyecto']).exists():
        tarea = Tarea.objects.create(**tarea_data)
        tareas.append(tarea)
        print(f"✅ Tarea creada: {tarea.titulo}")
    else:
        tarea = Tarea.objects.filter(titulo=tarea_data['titulo'], proyecto=tarea_data['proyecto']).first()
        tareas.append(tarea)
        print(f"ℹ️  Tarea ya existe: {tarea.titulo}")

# Crear algunos comentarios
print("\n💬 Creando comentarios...")
comentarios_data = [
    {
        'tarea': tareas[1],
        'autor': usuarios[1],
        'contenido': '¿Ya revisaste la documentación de DRF para los filtros?',
    },
    {
        'tarea': tareas[1],
        'autor': usuarios[0],
        'contenido': 'Sí, ya implementé filtros básicos. Falta agregar paginación.',
    },
    {
        'tarea': tareas[5],
        'autor': usuarios[2],
        'contenido': 'Recomiendo usar Stripe porque tiene mejor documentación para React Native.',
    },
    {
        'tarea': tareas[7],
        'autor': admin,
        'contenido': 'El hosting debe estar listo antes del viernes para empezar las pruebas.',
    },
]

for comentario_data in comentarios_data:
    try:
        if not Comentario.objects.filter(
            tarea=comentario_data['tarea'],
            autor=comentario_data['autor'],
            contenido=comentario_data['contenido']
        ).exists():
            comentario = Comentario.objects.create(**comentario_data)
            print(f"✅ Comentario creado en: {comentario.tarea.titulo}")
    except Exception as e:
        print(f"⚠️  Error creando comentario: {e}")

print("\n" + "="*60)
print("✨ ¡Datos de prueba creados exitosamente!")
print("="*60)
print("\n📊 RESUMEN:")
print(f"   👥 Usuarios: {User.objects.count()}")
print(f"   📁 Proyectos: {Proyecto.objects.count()}")
print(f"   📝 Tareas: {Tarea.objects.count()}")
print(f"   💬 Comentarios: {Comentario.objects.count()}")
print("\n🔑 CREDENCIALES DE ACCESO:")
print("   Admin: admin / admin123")
print("   Usuarios: andres, maria, carlos, laura / password123")
print("\n🌐 Accede a: http://127.0.0.1:8000/cuentas/login/")
print("="*60)
