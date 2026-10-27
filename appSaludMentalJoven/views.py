from django.shortcuts import render

def index(request):
    """
    Vista provisional para la página de inicio.
    Renderiza la plantilla index.html directamente ubicada en la carpeta templates/.
    """
    context = {
        'titulo': 'Salud Mental Joven',
        'mensaje': 'Estructura Django configurada al estilo del proyecto de la asignatura.',
    }
    return render(request, 'index.html', context)
