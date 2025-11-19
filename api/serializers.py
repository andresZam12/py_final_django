from rest_framework import serializers
from proyectos.models import Proyecto, Tarea, Comentario, Historial, Notificacion
from cuentas.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class ProyectoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Proyecto"""
    creado_por = UserSerializer(read_only=True)
    miembros = UserSerializer(many=True, read_only=True)
    progreso = serializers.ReadOnlyField()
    total_tareas = serializers.SerializerMethodField()
    
    class Meta:
        model = Proyecto
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_total_tareas(self, obj):
        return obj.tareas.count()


class TareaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Tarea"""
    asignado_a = UserSerializer(read_only=True)
    creado_por = UserSerializer(read_only=True)
    proyecto_nombre = serializers.CharField(source='proyecto.nombre', read_only=True)
    esta_vencida = serializers.ReadOnlyField()
    dias_restantes = serializers.ReadOnlyField()
    
    class Meta:
        model = Tarea
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Comentario"""
    usuario = UserSerializer(read_only=True)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    
    class Meta:
        model = Comentario
        fields = '__all__'
        read_only_fields = ['fecha']


class HistorialSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Historial"""
    usuario = UserSerializer(read_only=True)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    
    class Meta:
        model = Historial
        fields = '__all__'
        read_only_fields = ['fecha']


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Notificacion"""
    usuario = UserSerializer(read_only=True)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = '__all__'
        read_only_fields = ['fecha_creacion']
