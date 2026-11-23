from django.shortcuts import render, get_object_or_404
from .models import Categoria, Tematica, Formato, Articulo, Actividad, RecursoAyuda


def index(request):
    # Un recurso de ayuda por cada formato (el primero de cada uno)
    recursos_por_formato = []
    for formato in Formato.objects.all():
        recurso = formato.recursos.first()
        if recurso:
            recursos_por_formato.append(recurso)

    return render(request, 'index.html', {
        'recursos_por_formato': recursos_por_formato,
        'articulos': Articulo.objects.prefetch_related('categorias')[:3],
        'actividades': Actividad.objects.all()[:3],
    })


# --- MÓDULO ARTÍCULOS ---
def lista_articulos(request):
    return render(request, 'articulos_list.html', {
        'articulos': Articulo.objects.prefetch_related('categorias'),
    })


def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    return render(request, 'articulo_detail.html', {'articulo': articulo})


# --- MÓDULO CATEGORÍAS ---
def lista_categorias(request):
    return render(request, 'categorias_list.html', {
        'categorias': Categoria.objects.all(),
    })


def detalle_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    return render(request, 'categoria_detail.html', {
        'categoria': categoria,
        'articulos': categoria.articulos.prefetch_related('categorias'),
    })


# --- MÓDULO TEMÁTICAS ---
def detalle_tematica(request, tematica_id):
    tematica = get_object_or_404(Tematica, pk=tematica_id)
    return render(request, 'tematica_detail.html', {
        'tematica': tematica,
        'articulos': tematica.articulos.all(),
        'actividades': tematica.actividades.all(),
        'recursos': tematica.recursos.select_related('formato'),
    })


# --- MÓDULO ACTIVIDADES ---
def lista_actividades(request):
    actividades = Actividad.objects.all()
    return render(request, 'actividades_list.html', {'actividades': actividades})


def detalle_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    return render(request, 'actividad_detail.html', {'actividad': actividad})


# --- MÓDULO RECURSOS DE AYUDA ---
def lista_recursos(request):
    recursos = RecursoAyuda.objects.select_related('formato')
    return render(request, 'recursos_list.html', {'recursos': recursos})


def detalle_recurso(request, recurso_id):
    recurso = get_object_or_404(RecursoAyuda, pk=recurso_id)
    return render(request, 'recurso_detail.html', {'recurso': recurso})
