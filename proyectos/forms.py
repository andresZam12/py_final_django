from django import forms
from .models import Proyecto, Tarea, Comentario

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['proyecto', 'titulo', 'descripcion', 'asignado_a', 'fecha_limite', 'estado']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
