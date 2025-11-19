"""
Script para actualizar permisos de usuarios según su rol
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONTROL_PY_TAREAS.settings')
django.setup()

from cuentas.models import User

# Actualizar todos los usuarios
users = User.objects.all()
for user in users:
    if user.role == 'admin':
        user.is_staff = True
        user.is_superuser = True
        print(f"✅ {user.username} - Configurado como ADMIN (is_staff=True, is_superuser=True)")
    else:
        user.is_staff = False
        user.is_superuser = False
        print(f"👤 {user.username} - Configurado como MEMBER (is_staff=False, is_superuser=False)")
    user.save()

print("\n✅ Permisos actualizados correctamente")
