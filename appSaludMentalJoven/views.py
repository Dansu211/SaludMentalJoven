from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import InscripcionForm
from .models import Actividad, Articulo, Categoria, Formato, RecursoAyuda, Tematica


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Un recurso de ayuda por cada formato (el primero de cada uno)
        recursos_por_formato = []
        for formato in Formato.objects.prefetch_related('recursos'):
            recurso = next(iter(formato.recursos.all()), None)
            if recurso:
                recursos_por_formato.append(recurso)
        context['recursos_por_formato'] = recursos_por_formato
        context['articulos'] = Articulo.objects.prefetch_related('categorias')[:3]
        context['actividades'] = Actividad.objects.all()[:3]
        return context


# --- MÓDULO ARTÍCULOS ---
class ArticuloListView(ListView):
    model = Articulo
    template_name = 'articulos_list.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        return Articulo.objects.prefetch_related('categorias')


class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'articulo_detail.html'
    context_object_name = 'articulo'
    pk_url_kwarg = 'articulo_id'


class ArticuloBusquedaView(View):
    """Endpoint AJAX: devuelve en JSON los artículos que coinciden con ?q=..."""

    def get(self, request):
        q = request.GET.get('q', '').strip()
        articulos = Articulo.objects.prefetch_related('categorias')
        if q:
            articulos = articulos.filter(
                Q(titulo__icontains=q) | Q(resumen__icontains=q) | Q(contenido__icontains=q)
            )
        datos = [{
            'titulo': a.titulo,
            'resumen': a.resumen,
            'url': reverse('appSaludMentalJoven:detalle_articulo', args=[a.pk]),
            'categorias': [c.nombre for c in a.categorias.all()],
        } for a in articulos]
        return JsonResponse({'consulta': q, 'total': len(datos), 'articulos': datos})


# --- MÓDULO CATEGORÍAS ---
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categorias_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.annotate(num_articulos=Count('articulos'))


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'categoria_detail.html'
    context_object_name = 'categoria'
    pk_url_kwarg = 'categoria_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.object.articulos.prefetch_related('categorias')
        return context


# --- MÓDULO TEMÁTICAS ---
class TematicaDetailView(DetailView):
    model = Tematica
    template_name = 'tematica_detail.html'
    context_object_name = 'tematica'
    pk_url_kwarg = 'tematica_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.object.articulos.all()
        context['actividades'] = self.object.actividades.all()
        context['recursos'] = self.object.recursos.select_related('formato')
        return context


# --- MÓDULO ACTIVIDADES ---
class ActividadListView(ListView):
    model = Actividad
    template_name = 'actividades_list.html'
    context_object_name = 'actividades'


class ActividadDetailView(FormMixin, DetailView):
    """Detalle de la actividad + formulario de inscripción (ModelForm).

    Si la petición llega por AJAX (cabecera X-Requested-With) responde en JSON;
    si no, funciona como un formulario normal con redirección (progressive enhancement).
    """
    model = Actividad
    template_name = 'actividad_detail.html'
    context_object_name = 'actividad'
    pk_url_kwarg = 'actividad_id'
    form_class = InscripcionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['actividad'] = self.object
        return kwargs

    def get_success_url(self):
        return reverse('appSaludMentalJoven:detalle_actividad', args=[self.object.pk])

    def es_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        inscripcion = form.save(commit=False)
        inscripcion.actividad = self.object
        inscripcion.save()
        mensaje = _('¡Inscripción completada, %(nombre)s! Te esperamos.') % {'nombre': inscripcion.nombre}
        if self.es_ajax():
            return JsonResponse({'ok': True, 'mensaje': mensaje, 'plazas_libres': self.object.plazas_libres})
        messages.success(self.request, mensaje)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        if self.es_ajax():
            return JsonResponse({'ok': False, 'errores': form.errors.get_json_data()}, status=400)
        return self.render_to_response(self.get_context_data(form=form))


# --- MÓDULO RECURSOS DE AYUDA ---
class RecursoListView(ListView):
    model = RecursoAyuda
    template_name = 'recursos_list.html'
    context_object_name = 'recursos'

    def get_queryset(self):
        return RecursoAyuda.objects.select_related('formato').prefetch_related('tematicas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatos'] = Formato.objects.all()
        return context


class RecursoDetailView(DetailView):
    model = RecursoAyuda
    template_name = 'recurso_detail.html'
    context_object_name = 'recurso'
    pk_url_kwarg = 'recurso_id'

    def get_queryset(self):
        return RecursoAyuda.objects.select_related('formato')
