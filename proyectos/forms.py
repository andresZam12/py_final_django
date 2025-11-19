from django import forms
from .models import Proyecto, Tarea, Comentario
from django.core.exceptions import ValidationError
from django.utils import timezone


class ProyectoForm(forms.ModelForm):
    """
    Formulario para crear/editar proyectos
    """
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del proyecto'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio')
        
        return cleaned_data


class TareaForm(forms.ModelForm):
    """
    Formulario para crear/editar tareas
    """
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'proyecto', 'asignado_a', 'prioridad', 'estado', 'fecha_limite']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción de la tarea'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'asignado_a': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_limite': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_fecha_limite(self):
        fecha_limite = self.cleaned_data.get('fecha_limite')
        
        # Validar que la fecha límite no sea en el pasado (solo para nuevas tareas)
        if not self.instance.pk:  # Solo si es una tarea nueva
            if fecha_limite < timezone.now().date():
                raise ValidationError('La fecha límite no puede ser en el pasado')
        
        return fecha_limite
    
    def clean(self):
        cleaned_data = super().clean()
        proyecto = cleaned_data.get('proyecto')
        fecha_limite = cleaned_data.get('fecha_limite')
        
        # Validar que la fecha límite esté dentro del rango del proyecto
        if proyecto and fecha_limite:
            if fecha_limite < proyecto.fecha_inicio:
                raise ValidationError('La fecha límite no puede ser anterior al inicio del proyecto')
            if proyecto.fecha_fin and fecha_limite > proyecto.fecha_fin:
                raise ValidationError('La fecha límite no puede ser posterior al fin del proyecto')
        
        return cleaned_data


class TareaMemberForm(forms.ModelForm):
    """
    Formulario simplificado para members - Solo pueden cambiar el estado
    """
    class Meta:
        model = Tarea
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].label = 'Estado de la tarea'
        self.fields['estado'].help_text = 'Solo puedes cambiar el estado de tu tarea asignada'


class ComentarioForm(forms.ModelForm):
    """
    Formulario para agregar comentarios a tareas
    """
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }
    
    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        
        if len(contenido) < 10:
            raise ValidationError('El comentario debe tener al menos 10 caracteres')
        
        return contenido


class BusquedaAvanzadaForm(forms.Form):
    """
    Formulario para búsqueda avanzada de tareas
    """
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar tareas...'
        })
    )
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Tarea.ESTADOS),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    prioridad = forms.ChoiceField(
        choices=[('', 'Todas')] + list(Tarea.PRIORIDADES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
