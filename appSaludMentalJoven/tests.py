from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone, translation

from .models import Actividad, Articulo, Categoria, Inscripcion


class BaseTest(TestCase):
    fixtures = ['datos_iniciales.json']

    def setUp(self):
        translation.activate('es')
        self.actividad = Actividad.objects.create(
            titulo='Taller de prueba', descripcion='Desc', fecha=timezone.now() + timedelta(days=7),
            lugar='Online', plazas=1)
        self.url_actividad = reverse('appSaludMentalJoven:detalle_actividad', args=[self.actividad.pk])


class VistasTest(BaseTest):
    def test_paginas_publicas_responden(self):
        nombres = ['index', 'articulos', 'categorias', 'actividades', 'recursos']
        for nombre in nombres:
            self.assertEqual(self.client.get(reverse(f'appSaludMentalJoven:{nombre}')).status_code, 200)

    def test_detalle_inexistente_da_404(self):
        url = reverse('appSaludMentalJoven:detalle_articulo', args=[9999])
        self.assertEqual(self.client.get(url).status_code, 404)


class InscripcionTest(BaseTest):
    datos = {'nombre': 'Ane', 'email': 'ane@example.com', 'edad': 18, 'comentario': ''}

    def test_inscripcion_normal_redirige(self):
        r = self.client.post(self.url_actividad, self.datos)
        self.assertRedirects(r, self.url_actividad)
        self.assertEqual(self.actividad.inscripciones.count(), 1)

    def test_inscripcion_ajax_devuelve_json(self):
        r = self.client.post(self.url_actividad, self.datos, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])
        self.assertEqual(r.json()['plazas_libres'], 0)

    def test_edad_fuera_de_rango(self):
        r = self.client.post(self.url_actividad, {**self.datos, 'edad': 50},
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 400)
        self.assertIn('edad', r.json()['errores'])

    def test_sin_plazas(self):
        Inscripcion.objects.create(actividad=self.actividad, nombre='X', email='x@example.com', edad=20)
        r = self.client.post(self.url_actividad, self.datos, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 400)
        self.assertIn('__all__', r.json()['errores'])


class ActividadFinalizadaTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.pasada = Actividad.objects.create(
            titulo='Taller pasado', descripcion='Desc', fecha=timezone.now() - timedelta(days=1),
            lugar='Online', plazas=10)

    def test_no_admite_inscripciones(self):
        url = reverse('appSaludMentalJoven:detalle_actividad', args=[self.pasada.pk])
        r = self.client.post(url, InscripcionTest.datos, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.pasada.inscripciones.count(), 0)

    def test_no_sale_en_proximas_de_la_portada(self):
        r = self.client.get(reverse('appSaludMentalJoven:index'))
        self.assertNotIn(self.pasada, r.context['actividades'])
        self.assertIn(self.actividad, r.context['actividades'])


class MenuActivoTest(BaseTest):
    def test_marca_la_seccion_actual(self):
        r = self.client.get(reverse('appSaludMentalJoven:articulos'))
        self.assertContains(r, 'class="active" aria-current="page">Artículos')


class BusquedaAjaxTest(BaseTest):
    def test_busqueda_filtra(self):
        cat = Categoria.objects.first()
        art = Articulo.objects.create(titulo='Zzz único', resumen='r', contenido='c')
        art.categorias.add(cat)
        r = self.client.get(reverse('appSaludMentalJoven:buscar_articulos'), {'q': 'Zzz'})
        self.assertEqual(r.json()['total'], 1)
        self.assertEqual(r.json()['articulos'][0]['titulo'], 'Zzz único')


class I18nTest(BaseTest):
    def test_ingles(self):
        r = self.client.get('/en/')
        self.assertContains(r, 'Latest articles')
        self.assertContains(r, '<html lang="en">')

    def test_espanol(self):
        self.assertContains(self.client.get('/es/'), 'Últimos artículos')
