from django.contrib import admin
from .models import Proyecto, Tarea, Comentario, Historial

admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Comentario)
admin.site.register(Historial)
