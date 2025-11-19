from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from proyectos.models import Proyecto, Tarea, Notificacion


def home(request):
    """Vista de página de inicio"""
    if request.user.is_authenticated:
        return redirect('panel:dashboard')
    return render(request, 'panel/home.html')


@login_required
def dashboard(request):
    """Vista del dashboard principal con estadísticas"""
    user = request.user
    
    # Estadísticas generales
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    mis_proyectos = Proyecto.objects.filter(
        Q(creado_por=user) | Q(miembros=user)
    ).distinct().count()
    
    # Estadísticas de tareas
    total_tareas = Tarea.objects.count()
    mis_tareas = user.tareas_asignadas.count()
    tareas_pendientes = user.tareas_asignadas.filter(estado='pendiente').count()
    tareas_en_progreso = user.tareas_asignadas.filter(estado='en_progreso').count()
    tareas_completadas = user.tareas_asignadas.filter(estado='completada').count()
    
    # Tareas próximas a vencer (próximos 7 días)
    fecha_limite = timezone.now().date() + timedelta(days=7)
    tareas_proximas = user.tareas_asignadas.filter(
        fecha_limite__lte=fecha_limite,
        fecha_limite__gte=timezone.now().date(),
        estado__in=['pendiente', 'en_progreso']
    ).order_by('fecha_limite')[:5]
    
    # Tareas vencidas
    tareas_vencidas = user.tareas_asignadas.filter(
        fecha_limite__lt=timezone.now().date(),
        estado__in=['pendiente', 'en_progreso']
    ).count()
    
    # Notificaciones no leídas
    notificaciones_count = user.notificaciones.filter(leida=False).count()
    notificaciones_recientes = user.notificaciones.filter(leida=False).order_by('-fecha_creacion')[:5]
    
    # Proyectos recientes
    proyectos_recientes = Proyecto.objects.filter(
        Q(creado_por=user) | Q(miembros=user)
    ).distinct().order_by('-fecha_creacion')[:5]
    
    # Actividad reciente (últimos 10 cambios)
    from proyectos.models import Historial
    actividad_reciente = Historial.objects.filter(
        Q(tarea__proyecto__creado_por=user) | Q(tarea__proyecto__miembros=user)
    ).distinct().order_by('-fecha')[:10]
    
    # Datos para gráficos
    # Tareas por estado
    tareas_por_estado = {
        'pendiente': Tarea.objects.filter(estado='pendiente').count(),
        'en_progreso': Tarea.objects.filter(estado='en_progreso').count(),
        'completada': Tarea.objects.filter(estado='completada').count(),
    }
    
    # Tareas por prioridad
    tareas_por_prioridad = {
        'baja': Tarea.objects.filter(prioridad='baja').count(),
        'media': Tarea.objects.filter(prioridad='media').count(),
        'alta': Tarea.objects.filter(prioridad='alta').count(),
    }
    
    context = {
        # Estadísticas
        'total_proyectos': total_proyectos,
        'mis_proyectos': mis_proyectos,
        'total_tareas': total_tareas,
        'mis_tareas': mis_tareas,
        'tareas_pendientes': tareas_pendientes,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_completadas': tareas_completadas,
        'tareas_vencidas': tareas_vencidas,
        'notificaciones_count': notificaciones_count,
        
        # Listas
        'tareas_proximas': tareas_proximas,
        'notificaciones_recientes': notificaciones_recientes,
        'proyectos_recientes': proyectos_recientes,
        'actividad_reciente': actividad_reciente,
        
        # Datos para gráficos (JSON)
        'tareas_por_estado': tareas_por_estado,
        'tareas_por_prioridad': tareas_por_prioridad,
    }
    
    return render(request, 'panel/home.html', context)


@login_required
def estadisticas_json(request):
    """
    Vista que retorna estadísticas en formato JSON para gráficos dinámicos
    """
    # Tareas por estado
    tareas_por_estado = {
        'labels': ['Pendientes', 'En Progreso', 'Completadas'],
        'data': [
            Tarea.objects.filter(estado='pendiente').count(),
            Tarea.objects.filter(estado='en_progreso').count(),
            Tarea.objects.filter(estado='completada').count(),
        ]
    }
    
    # Tareas por prioridad
    tareas_por_prioridad = {
        'labels': ['Baja', 'Media', 'Alta'],
        'data': [
            Tarea.objects.filter(prioridad='baja').count(),
            Tarea.objects.filter(prioridad='media').count(),
            Tarea.objects.filter(prioridad='alta').count(),
        ]
    }
    
    # Proyectos por mes (últimos 6 meses)
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta
    
    seis_meses_atras = timezone.now() - timedelta(days=180)
    proyectos_por_mes = Proyecto.objects.filter(
        fecha_creacion__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('fecha_creacion')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    meses_labels = []
    meses_data = []
    for item in proyectos_por_mes:
        mes_nombre = item['mes'].strftime('%B %Y')
        meses_labels.append(mes_nombre)
        meses_data.append(item['total'])
    
    proyectos_mensuales = {
        'labels': meses_labels,
        'data': meses_data
    }
    
    # Tareas del usuario actual por estado
    mis_tareas_estado = {
        'labels': ['Pendientes', 'En Progreso', 'Completadas'],
        'data': [
            request.user.tareas_asignadas.filter(estado='pendiente').count(),
            request.user.tareas_asignadas.filter(estado='en_progreso').count(),
            request.user.tareas_asignadas.filter(estado='completada').count(),
        ]
    }
    
    data = {
        'tareas_por_estado': tareas_por_estado,
        'tareas_por_prioridad': tareas_por_prioridad,
        'proyectos_mensuales': proyectos_mensuales,
        'mis_tareas_estado': mis_tareas_estado,
    }
    
    return JsonResponse(data)
