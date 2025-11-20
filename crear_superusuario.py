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
    # Solo crear si no existe
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'  # Campo requerido por el modelo personalizado
        )
        print('✓ Superusuario creado exitosamente: admin / admin123')
    else:
        print('✓ El superusuario admin ya existe')
except Exception as e:
    print(f'✗ Error al crear superusuario: {e}')
    sys.exit(1)
