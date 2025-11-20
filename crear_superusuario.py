#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONTROL_PY_TAREAS.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Crear o actualizar el superusuario
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    if created:
        user.set_password('admin123')
        user.save()
        print('✓ Superusuario creado exitosamente: admin / admin123')
    else:
        # Actualizar si ya existe pero no tiene permisos
        if not user.is_staff or not user.is_superuser:
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password('admin123')
            user.save()
            print('✓ Superusuario actualizado con permisos correctos: admin / admin123')
        else:
            print('✓ El superusuario admin ya existe con permisos correctos')
except Exception as e:
    print(f'✗ Error al crear/actualizar superusuario: {e}')
    sys.exit(1)
