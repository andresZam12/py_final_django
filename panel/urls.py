from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('estadisticas/', views.estadisticas_json, name='estadisticas_json'),
]
