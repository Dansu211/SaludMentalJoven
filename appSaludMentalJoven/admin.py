from django.contrib import admin
from .models import Categoria, Tematica, Formato, Articulo, Actividad, Inscripcion, RecursoAyuda


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


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ('fecha_inscripcion',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar', 'plazas', 'plazas_libres')
    list_filter = ('tematicas',)
    filter_horizontal = ('tematicas',)
    inlines = [InscripcionInline]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'edad', 'actividad', 'fecha_inscripcion')
    list_filter = ('actividad',)
    search_fields = ('nombre', 'email')


@admin.register(RecursoAyuda)
class RecursoAyudaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'formato', 'telefono', 'horario', 'web')
    list_filter = ('formato', 'tematicas')
    filter_horizontal = ('tematicas',)
