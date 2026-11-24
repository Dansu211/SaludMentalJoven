from django.urls import path
from . import views

app_name = 'appSaludMentalJoven'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # Artículos
    path('articulos/', views.ArticuloListView.as_view(), name='articulos'),
    path('articulos/buscar/', views.ArticuloBusquedaView.as_view(), name='buscar_articulos'),
    path('articulos/<int:articulo_id>/', views.ArticuloDetailView.as_view(), name='detalle_articulo'),
    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categorias'),
    path('categorias/<int:categoria_id>/', views.CategoriaDetailView.as_view(), name='detalle_categoria'),
    # Temáticas
    path('tematicas/<int:tematica_id>/', views.TematicaDetailView.as_view(), name='detalle_tematica'),
    # Actividades (el detalle incluye el formulario de inscripción)
    path('actividades/', views.ActividadListView.as_view(), name='actividades'),
    path('actividades/<int:actividad_id>/', views.ActividadDetailView.as_view(), name='detalle_actividad'),
    # Recursos de ayuda
    path('recursos/', views.RecursoListView.as_view(), name='recursos'),
    path('recursos/<int:recurso_id>/', views.RecursoDetailView.as_view(), name='detalle_recurso'),
]
