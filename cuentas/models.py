from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('member', 'Miembro'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    def save(self, *args, **kwargs):
        # Solo los usuarios con rol 'admin' pueden acceder al panel de administración
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'member':
            # Solo quitar permisos si el rol es explícitamente 'member'
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
