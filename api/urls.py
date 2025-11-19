from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ProyectoViewSet, 
    TareaViewSet, 
    ComentarioViewSet, 
    HistorialViewSet,
    NotificacionViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'tareas', TareaViewSet, basename='tarea')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')
router.register(r'historial', HistorialViewSet, basename='historial')
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # Login/logout para API browsable
]
