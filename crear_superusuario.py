import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONTROL_PY_TAREAS.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Solo crear si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password=os.environ.get('ADMIN_PASSWORD', 'admin123')
    )
    print('Superusuario creado: admin')
else:
    print('El superusuario ya existe')
