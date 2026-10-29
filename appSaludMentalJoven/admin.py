from django.contrib import admin
from .models import Categoria, Articulo, Actividad, RecursoAyuda

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'fecha_publicacion')
    list_filter = ('categoria',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar', 'plazas')

@admin.register(RecursoAyuda)
class RecursoAyudaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'horario', 'web')