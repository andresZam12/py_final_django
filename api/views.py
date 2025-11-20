from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from proyectos.models import Proyecto, Tarea, Comentario, Historial, Notificacion
from cuentas.models import User
from .serializers import (
    ProyectoSerializer, 
    TareaSerializer, 
    ComentarioSerializer, 
    HistorialSerializer,
    NotificacionSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para usuarios (solo lectura)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']


class ProyectoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para proyectos con filtros, búsqueda y ordenamiento
    """
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creado_por', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_inicio', 'fecha_fin', 'nombre']
    ordering = ['-fecha_inicio']
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como creador"""
        serializer.save(creado_por=self.request.user)
    
    @action(detail=True, methods=['get'])
    def tareas(self, request, pk=None):
        """
        Endpoint personalizado para obtener todas las tareas de un proyecto
        """
        proyecto = self.get_object()
        tareas = proyecto.tareas.all()
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """
        Endpoint para estadísticas del proyecto
        """
        proyecto = self.get_object()
        return Response({
            'progreso': proyecto.calcular_progreso(),
            'esta_atrasado': proyecto.esta_atrasado(),
            'total_tareas': proyecto.tareas.count(),
            'tareas_completadas': proyecto.tareas.filter(estado='completada').count(),
            'tareas_pendientes': proyecto.tareas.filter(estado='pendiente').count(),
            'tareas_en_progreso': proyecto.tareas.filter(estado='en_progreso').count(),
        })


class TareaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para tareas con filtros avanzados
    """
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['proyecto', 'asignado_a', 'estado', 'prioridad', 'fecha_limite']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_limite', 'prioridad', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como creador"""
        tarea = serializer.save(creado_por=self.request.user)
        # Pasar el usuario actual para el historial
        tarea._current_user = self.request.user
        tarea.save()
    
    def get_queryset(self):
        """
        Filtro adicional por usuario asignado
        """
        queryset = super().get_queryset()
        asignado_a = self.request.query_params.get('asignado_a', None)
        if asignado_a:
            queryset = queryset.filter(asignado_a_id=asignado_a)
        return queryset
    
    @action(detail=False, methods=['get'])
    def mis_tareas(self, request):
        """
        Endpoint para obtener tareas del usuario autenticado
        """
        tareas = Tarea.objects.filter(asignado_a=request.user)
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def proximas_vencer(self, request):
        """
        Endpoint para tareas próximas a vencer (7 días)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        fecha_limite = timezone.now().date() + timedelta(days=7)
        tareas = Tarea.objects.filter(
            fecha_limite__lte=fecha_limite,
            estado__in=['pendiente', 'en_progreso']
        )
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)


class ComentarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para comentarios
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tarea', 'autor']
    search_fields = ['contenido']
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual como autor"""
        serializer.save(autor=self.request.user)


class HistorialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para historial (solo lectura)
    """
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tarea', 'usuario', 'accion']
    ordering_fields = ['fecha']
    ordering = ['-fecha']


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para notificaciones
    """
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['usuario', 'leido']
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        """
        Filtrar solo notificaciones del usuario autenticado
        """
        return Notificacion.objects.filter(usuario=self.request.user)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """
        Marcar todas las notificaciones como leídas
        """
        count = Notificacion.objects.filter(usuario=request.user, leido=False).update(leido=True)
        return Response({'mensaje': f'{count} notificaciones marcadas como leídas'})
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """
        Marcar una notificación como leída
        """
        notificacion = self.get_object()
        notificacion.leido = True
        notificacion.save()
        return Response({'mensaje': 'Notificación marcada como leída'})
