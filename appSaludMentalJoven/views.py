from django.shortcuts import render, get_object_or_404
from .models import Categoria, Articulo, Actividad, RecursoAyuda

def index(request):
    return render(request, 'index.html', {
        'articulos': Articulo.objects.all()[:3],
        'actividades': Actividad.objects.all()[:3],
        'recursos': RecursoAyuda.objects.all()[:3],
    })

def lista_articulos(request):
    return render(request, 'articulos_list.html', {
        'articulos': Articulo.objects.all(),
        'categorias': Categoria.objects.all()
    })

def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    return render(request, 'articulo_detail.html', {'articulo': articulo})

def articulos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    return render(request, 'articulos_list.html', {
        'articulos': categoria.articulos.all(),
        'categorias': Categoria.objects.all(),
        'categoria_actual': categoria
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
    recursos = RecursoAyuda.objects.all()
    return render(request, 'recursos_list.html', {'recursos': recursos})