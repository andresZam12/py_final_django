from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    # Proyectos
    path('', views.ProyectoListView.as_view(), name='proyecto_list'),
    path('proyecto/<int:pk>/', views.ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('proyecto/nuevo/', views.ProyectoCreateView.as_view(), name='proyecto_create'),
    path('proyecto/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('proyecto/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='proyecto_delete'),
    
    # Tareas
    path('tareas/', views.TareaListView.as_view(), name='tarea_list'),
    path('tarea/<int:pk>/', views.TareaDetailView.as_view(), name='tarea_detail'),
    path('tarea/nueva/', views.TareaCreateView.as_view(), name='tarea_create'),
    path('tarea/<int:pk>/editar/', views.TareaUpdateView.as_view(), name='tarea_update'),
    path('tarea/<int:pk>/eliminar/', views.TareaDeleteView.as_view(), name='tarea_delete'),
    path('tarea/<int:tarea_id>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    
    # Mis tareas
    path('mis-tareas/', views.mis_tareas, name='mis_tareas'),
]
