from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('documento', 'nombre_completo', 'sexo', 'is_staff', 'fecha_registro')
    search_fields = ('documento', 'nombre_completo')

# Register your models here.
