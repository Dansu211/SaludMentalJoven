from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título del artículo")
    resumen = models.CharField(max_length=300, verbose_name="Resumen")
    contenido = models.TextField(verbose_name="Contenido completo")
    autor = models.CharField(max_length=100, default="Equipo SMJ", verbose_name="Autor/a")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='articulos', verbose_name="Categoría")
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de publicación")

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo


class Actividad(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título de la actividad")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha = models.DateTimeField(verbose_name="Fecha y hora")
    lugar = models.CharField(max_length=200, verbose_name="Lugar o modalidad")
    plazas = models.PositiveIntegerField(default=20, verbose_name="Plazas")

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['fecha']

    def __str__(self):
        return self.titulo


class RecursoAyuda(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la entidad")
    descripcion = models.TextField(verbose_name="Descripción")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    web = models.URLField(blank=True, verbose_name="Sitio web")
    horario = models.CharField(max_length=100, default="24/7", verbose_name="Horario")

    class Meta:
        verbose_name = "Recurso de Ayuda"
        verbose_name_plural = "Recursos de Ayuda"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre