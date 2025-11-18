from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from .forms import ProyectoForm

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/lista_proyectos.html', {'proyectos': proyectos})


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creado_por = request.user
            proyecto.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()

    return render(request, 'proyectos/crear_proyecto.html', {'form': form})


def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'proyectos/editar_proyecto.html', {'form': form})


def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    if request.method == 'POST':
        proyecto.delete()
        return redirect('lista_proyectos')

    return render(request, 'proyectos/eliminar_proyecto.html', {'proyecto': proyecto})
