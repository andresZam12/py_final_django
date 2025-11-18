from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('editar/<int:id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
]
