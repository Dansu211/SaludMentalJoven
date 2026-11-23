from django.contrib import admin
from .models import Categoria, Tematica, Formato, Articulo, Actividad, RecursoAyuda


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Tematica)
class TematicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Formato)
class FormatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    list_filter = ('categorias', 'tematicas')
    filter_horizontal = ('categorias', 'tematicas')


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar', 'plazas')
    list_filter = ('tematicas',)
    filter_horizontal = ('tematicas',)


@admin.register(RecursoAyuda)
class RecursoAyudaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'formato', 'telefono', 'horario', 'web')
    list_filter = ('formato', 'tematicas')
    filter_horizontal = ('tematicas',)
