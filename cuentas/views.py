from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import User


def login_view(request):
    """
    Vista de login personalizada
    """
    if request.user.is_authenticated:
        return redirect('panel:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            next_url = request.GET.get('next', 'panel:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'cuentas/login.html')


@login_required
def logout_view(request):
    """
    Vista de logout
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('cuentas:login')


def registro_view(request):
    """
    Vista de registro de usuarios
    """
    if request.user.is_authenticated:
        return redirect('panel:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role', 'member')
        
        # Validaciones
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'cuentas/registro.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'cuentas/registro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'cuentas/registro.html')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        messages.success(request, 'Registro exitoso. Por favor inicia sesión')
        return redirect('cuentas:login')
    
    return render(request, 'cuentas/registro.html')


@login_required
def perfil_view(request):
    """
    Vista de perfil del usuario
    """
    from proyectos.models import Tarea, Proyecto
    
    tareas_asignadas = Tarea.objects.filter(asignado_a=request.user)
    proyectos_creados = Proyecto.objects.filter(creado_por=request.user)
    
    context = {
        'tareas_asignadas': tareas_asignadas,
        'proyectos_creados': proyectos_creados,
    }
    
    return render(request, 'cuentas/perfil.html', context)
