from django.urls import path
from . import views

app_name = 'appSaludMentalJoven'

urlpatterns = [
    path('', views.index, name='index'),
    # Artículos
    path('articulos/', views.lista_articulos, name='articulos'),
    path('articulos/<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),
    # Categorías
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/<int:categoria_id>/', views.detalle_categoria, name='detalle_categoria'),
    # Temáticas
    path('tematicas/<int:tematica_id>/', views.detalle_tematica, name='detalle_tematica'),
    # Actividades
    path('actividades/', views.lista_actividades, name='actividades'),
    path('actividades/<int:actividad_id>/', views.detalle_actividad, name='detalle_actividad'),
    # Recursos de ayuda
    path('recursos/', views.lista_recursos, name='recursos'),
    path('recursos/<int:recurso_id>/', views.detalle_recurso, name='detalle_recurso'),
]
