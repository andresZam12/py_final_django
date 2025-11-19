from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Proyecto, Tarea, Comentario, Historial
from .forms import ProyectoForm, TareaForm, ComentarioForm, BusquedaAvanzadaForm


# ============ MIXINS DE PERMISOS ============

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin que verifica que el usuario sea administrador
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para realizar esta acción. Solo administradores.')
        return redirect('panel:dashboard')


class TareaOwnerOrAdminMixin(UserPassesTestMixin):
    """
    Mixin que verifica que el usuario sea el asignado de la tarea o un administrador
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        tarea = self.get_object()
        # Admin puede todo, member solo sus tareas asignadas
        return (self.request.user.role == 'admin' or 
                tarea.asignado_a == self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar esta tarea.')
        return redirect('proyectos:tarea_list')


# ============ VISTAS DE PROYECTOS ============

class ProyectoListView(LoginRequiredMixin, ListView):
    """
    Lista de proyectos
    """
    model = Proyecto
    template_name = 'proyectos/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get('busqueda', '')
        
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | 
                Q(descripcion__icontains=busqueda)
            )
        
        return queryset.order_by('-fecha_inicio')


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    """
    Detalle de un proyecto con sus tareas
    """
    model = Proyecto
    template_name = 'proyectos/proyecto_detail.html'
    context_object_name = 'proyecto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()
        tareas = proyecto.tareas.all()
        context['tareas'] = tareas.order_by('-fecha_creacion')
        context['progreso'] = proyecto.calcular_progreso()
        context['esta_atrasado'] = proyecto.esta_atrasado()
        # Contadores de tareas por estado
        context['tareas_completadas'] = tareas.filter(estado='completada').count()
        context['tareas_en_progreso'] = tareas.filter(estado='en_progreso').count()
        context['tareas_pendientes'] = tareas.filter(estado='pendiente').count()
        return context


class ProyectoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """
    Crear nuevo proyecto - SOLO ADMINS
    """
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')
    
    def form_valid(self, form):
        # Asignar el usuario actual como creador del proyecto
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Proyecto creado exitosamente')
        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """
    Actualizar proyecto existente - SOLO ADMINS
    """
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/proyecto_form.html'
    success_url = reverse_lazy('proyectos:proyecto_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Proyecto actualizado exitosamente')
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    Eliminar proyecto - SOLO ADMINS
    """
    model = Proyecto
    template_name = 'proyectos/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos:proyecto_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Proyecto eliminado exitosamente')
        return super().delete(request, *args, **kwargs)


# ============ VISTAS DE TAREAS ============

class TareaListView(LoginRequiredMixin, ListView):
    """
    Lista de tareas con filtros avanzados
    """
    model = Tarea
    template_name = 'proyectos/tarea_list.html'
    context_object_name = 'tareas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros del formulario de búsqueda avanzada
        busqueda = self.request.GET.get('busqueda', '')
        proyecto = self.request.GET.get('proyecto', '')
        estado = self.request.GET.get('estado', '')
        prioridad = self.request.GET.get('prioridad', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        
        if busqueda:
            queryset = queryset.filter(
                Q(titulo__icontains=busqueda) | 
                Q(descripcion__icontains=busqueda)
            )
        
        if proyecto:
            queryset = queryset.filter(proyecto_id=proyecto)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_limite__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha_limite__lte=fecha_hasta)
        
        return queryset.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BusquedaAvanzadaForm(self.request.GET or None)
        return context


class TareaDetailView(LoginRequiredMixin, DetailView):
    """
    Detalle de una tarea con comentarios e historial
    """
    model = Tarea
    template_name = 'proyectos/tarea_detail.html'
    context_object_name = 'tarea'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarea = self.get_object()
        context['comentarios'] = tarea.comentarios.all().order_by('-fecha')
        context['historial'] = tarea.historial.all().order_by('-fecha')
        context['comentario_form'] = ComentarioForm()
        return context


class TareaCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """
    Crear nueva tarea - SOLO ADMINS
    """
    model = Tarea
    form_class = TareaForm
    template_name = 'proyectos/tarea_form.html'
    
    def get_success_url(self):
        return reverse_lazy('proyectos:tarea_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        # Asignar el usuario actual como creador de la tarea
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Tarea creada exitosamente')
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        # Si viene desde un proyecto específico, pre-seleccionarlo
        proyecto_id = self.request.GET.get('proyecto')
        if proyecto_id:
            initial['proyecto'] = proyecto_id
        return initial


class TareaUpdateView(LoginRequiredMixin, TareaOwnerOrAdminMixin, UpdateView):
    """
    Actualizar tarea existente - Solo asignado o admin
    """
    model = Tarea
    form_class = TareaForm
    template_name = 'proyectos/tarea_form.html'
    
    def get_success_url(self):
        return reverse_lazy('proyectos:tarea_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarea actualizada exitosamente')
        return super().form_valid(form)


class TareaDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    Eliminar tarea - SOLO ADMINS
    """
    model = Tarea
    template_name = 'proyectos/tarea_confirm_delete.html'
    success_url = reverse_lazy('proyectos:tarea_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tarea eliminada exitosamente')
        return super().delete(request, *args, **kwargs)


# ============ VISTA PARA AGREGAR COMENTARIOS ============

@login_required
def agregar_comentario(request, tarea_id):
    """
    Agregar comentario a una tarea
    """
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tarea = tarea
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente')
        else:
            messages.error(request, 'Error al agregar el comentario')
    
    return redirect('proyectos:tarea_detail', pk=tarea_id)


@login_required
def mis_tareas(request):
    """
    Vista de tareas asignadas al usuario actual
    """
    tareas = Tarea.objects.filter(asignado_a=request.user).order_by('-fecha_creacion')
    
    # Contadores por estado
    tareas_pendientes = tareas.filter(estado='pendiente').count()
    tareas_en_progreso = tareas.filter(estado='en_progreso').count()
    tareas_completadas = tareas.filter(estado='completada').count()
    
    context = {
        'tareas': tareas,
        'titulo': 'Mis Tareas',
        'tareas_pendientes': tareas_pendientes,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_completadas': tareas_completadas,
    }
    
    return render(request, 'proyectos/mis_tareas.html', context)
