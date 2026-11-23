import django.db.models.deletion
from django.db import migrations, models


def copiar_categoria_a_categorias(apps, schema_editor):
    """Pasa la antigua FK Articulo.categoria a la nueva relación N:M."""
    Articulo = apps.get_model('appSaludMentalJoven', 'Articulo')
    for articulo in Articulo.objects.all():
        if articulo.categoria_id:
            articulo.categorias.add(articulo.categoria_id)


def copiar_categorias_a_categoria(apps, schema_editor):
    Articulo = apps.get_model('appSaludMentalJoven', 'Articulo')
    for articulo in Articulo.objects.all():
        primera = articulo.categorias.first()
        if primera:
            articulo.categoria = primera
            articulo.save(update_fields=['categoria'])


class Migration(migrations.Migration):

    dependencies = [
        ('appSaludMentalJoven', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre del formato')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Formato',
                'verbose_name_plural': 'Formatos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tematica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre de la temática')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Temática',
                'verbose_name_plural': 'Temáticas',
                'ordering': ['nombre'],
            },
        ),
        # Categoría–Artículo pasa de 1:N a N:M conservando los datos
        migrations.AlterField(
            model_name='articulo',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='appSaludMentalJoven.categoria', verbose_name='Categoría'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='categorias',
            field=models.ManyToManyField(related_name='articulos', to='appSaludMentalJoven.categoria', verbose_name='Categorías'),
        ),
        migrations.RunPython(copiar_categoria_a_categorias, copiar_categorias_a_categoria),
        migrations.RemoveField(
            model_name='articulo',
            name='categoria',
        ),
        # Temáticas (N:M) en artículos, actividades y recursos
        migrations.AddField(
            model_name='articulo',
            name='tematicas',
            field=models.ManyToManyField(blank=True, related_name='articulos', to='appSaludMentalJoven.tematica', verbose_name='Temáticas'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='tematicas',
            field=models.ManyToManyField(blank=True, related_name='actividades', to='appSaludMentalJoven.tematica', verbose_name='Temáticas'),
        ),
        migrations.AddField(
            model_name='recursoayuda',
            name='tematicas',
            field=models.ManyToManyField(blank=True, related_name='recursos', to='appSaludMentalJoven.tematica', verbose_name='Temáticas'),
        ),
        # Formato de cada recurso de ayuda
        migrations.AddField(
            model_name='recursoayuda',
            name='formato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recursos', to='appSaludMentalJoven.formato', verbose_name='Formato'),
        ),
        migrations.AlterField(
            model_name='recursoayuda',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, verbose_name='Teléfono'),
        ),
    ]
