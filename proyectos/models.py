from django.db import models
from django.conf import settings
from django.utils import timezone


class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proyectos_creados')
    miembros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='proyectos', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.nombre
    
    def progreso(self):
        """Calcula el porcentaje de tareas completadas"""
        total = self.tareas.count()
        if total == 0:
            return 0
        completadas = self.tareas.filter(estado='completada').count()
        return round((completadas / total) * 100, 2)
    
    def calcular_progreso(self):
        """Alias de progreso() para compatibilidad"""
        return self.progreso()
    
    def esta_atrasado(self):
        """Verifica si el proyecto está atrasado"""
        if self.fecha_fin:
            return timezone.now().date() > self.fecha_fin and self.progreso() < 100
        return False


class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tareas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_limite = models.DateField()
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.titulo
    
    def esta_vencida(self):
        """Verifica si la tarea está vencida"""
        return timezone.now().date() > self.fecha_limite and self.estado != 'completada'
    
    def dias_restantes(self):
        """Calcula días restantes hasta la fecha límite"""
        delta = self.fecha_limite - timezone.now().date()
        return delta.days


class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.tarea.titulo}"


class Historial(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'

    def __str__(self):
        return f"{self.accion} - {self.tarea.titulo}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    TIPOS = [
        ('asignacion', 'Asignación'),
        ('vencimiento', 'Próximo a Vencer'),
        ('cambio_estado', 'Cambio de Estado'),
        ('comentario', 'Nuevo Comentario'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"{self.tipo} - {self.usuario.username}"
