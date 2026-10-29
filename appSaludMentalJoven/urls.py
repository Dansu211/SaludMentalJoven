from django.urls import path
from . import views

app_name = 'appSaludMentalJoven'

urlpatterns = [
    path('', views.index, name='index'),
    # Artículos
    path('articulos/', views.lista_articulos, name='articulos'),
    path('articulos/<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),
    path('categorias/<int:categoria_id>/', views.articulos_por_categoria, name='articulos_categoria'),
    path('actividades/', views.lista_actividades, name='actividades'),
    path('actividades/<int:actividad_id>/', views.detalle_actividad, name='detalle_actividad'),
    path('recursos/', views.lista_recursos, name='recursos'),
]