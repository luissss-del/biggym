from django.contrib import admin
from .models import Usuario, DiaEntrenamiento, Ejercicio

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('documento', 'nombre_completo', 'sexo', 'is_staff', 'fecha_registro')
    search_fields = ('documento', 'nombre_completo')


@admin.register(DiaEntrenamiento)
class DiaEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dia', 'parte_cuerpo')


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dia_entrenamiento', 'repeticiones', 'completado')