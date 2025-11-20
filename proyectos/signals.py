from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Tarea, Historial, Notificacion


@receiver(pre_save, sender=Tarea)
def guardar_estado_anterior(sender, instance, **kwargs):
    """Guardar el estado anterior antes de modificar"""
    if instance.pk:
        try:
            old_instance = Tarea.objects.get(pk=instance.pk)
            instance._old_estado = old_instance.estado
            instance._old_asignado = old_instance.asignado_a
        except Tarea.DoesNotExist:
            pass


@receiver(post_save, sender=Tarea)
def crear_historial_tarea(sender, instance, created, **kwargs):
    """Crear registro en historial cuando se crea o modifica una tarea"""
    # Obtener el usuario que está haciendo la modificación desde el contexto de la tarea
    usuario_actual = getattr(instance, '_current_user', instance.creado_por)
    
    if created:
        # Historial de creación
        Historial.objects.create(
            tarea=instance,
            usuario=usuario_actual,
            accion=f"Tarea '{instance.titulo}' creada"
        )
        
        # Notificación de asignación si se asigna a alguien
        if instance.asignado_a:
            Notificacion.objects.create(
                usuario=instance.asignado_a,
                tarea=instance,
                mensaje=f"Se te ha asignado la tarea: {instance.titulo}",
                tipo='asignacion'
            )
    else:
        # Detectar cambios en el estado
        if hasattr(instance, '_old_estado') and instance._old_estado != instance.estado:
            Historial.objects.create(
                tarea=instance,
                usuario=usuario_actual,
                accion=f"Estado cambiado de '{instance._old_estado}' a '{instance.estado}'"
            )
            
            # Notificación de cambio de estado
            if instance.asignado_a:
                Notificacion.objects.create(
                    usuario=instance.asignado_a,
                    tarea=instance,
                    mensaje=f"El estado de '{instance.titulo}' cambió a {instance.get_estado_display()}",
                    tipo='cambio_estado'
                )
        
        # Detectar cambio de asignación
        if hasattr(instance, '_old_asignado') and instance._old_asignado != instance.asignado_a:
            if instance.asignado_a:
                Historial.objects.create(
                    tarea=instance,
                    usuario=usuario_actual,
                    accion=f"Tarea asignada a {instance.asignado_a.username}"
                )
                
                Notificacion.objects.create(
                    usuario=instance.asignado_a,
                    tarea=instance,
                    mensaje=f"Se te ha asignado la tarea: {instance.titulo}",
                    tipo='asignacion'
                )
