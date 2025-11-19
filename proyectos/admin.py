from django.contrib import admin
from .models import Proyecto, Tarea, Comentario, Historial, Notificacion


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creado_por', 'fecha_inicio', 'fecha_fin', 'progreso', 'esta_atrasado')
    list_filter = ('fecha_inicio', 'fecha_fin', 'creado_por')
    search_fields = ('nombre', 'descripcion')
    date_hierarchy = 'fecha_inicio'
    
    def progreso(self, obj):
        return f"{obj.progreso()}%"
    progreso.short_description = 'Progreso'
    
    def esta_atrasado(self, obj):
        from django.utils import timezone
        if obj.fecha_fin:
            return timezone.now().date() > obj.fecha_fin and obj.progreso() < 100
        return False
    esta_atrasado.boolean = True
    esta_atrasado.short_description = '¿Atrasado?'


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'asignado_a', 'estado', 'prioridad', 'fecha_limite')
    list_filter = ('estado', 'prioridad', 'fecha_limite', 'proyecto')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_limite'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'usuario', 'fecha', 'contenido_resumido')
    list_filter = ('fecha',)
    search_fields = ('contenido', 'usuario__username')
    date_hierarchy = 'fecha'
    
    def contenido_resumido(self, obj):
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    contenido_resumido.short_description = 'Contenido'


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'usuario', 'fecha', 'accion')
    list_filter = ('fecha', 'accion')
    search_fields = ('descripcion', 'usuario__username')
    date_hierarchy = 'fecha'


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje_resumido', 'leida', 'fecha_creacion')
    list_filter = ('leida', 'fecha_creacion')
    search_fields = ('mensaje', 'usuario__username')
    date_hierarchy = 'fecha_creacion'
    
    def mensaje_resumido(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_resumido.short_description = 'Mensaje'
