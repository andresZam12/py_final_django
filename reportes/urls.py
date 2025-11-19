from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reportes_index, name='index'),
    path('proyecto/<int:proyecto_id>/pdf/', views.reporte_proyecto_pdf, name='proyecto_pdf'),
    path('tareas/excel/', views.reporte_tareas_excel, name='tareas_excel'),
    path('general/excel/', views.reporte_general_excel, name='general_excel'),
]
