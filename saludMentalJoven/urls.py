from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # /i18n/setlang/ : vista de Django que cambia el idioma (formulario del selector)
    path('i18n/', include('django.conf.urls.i18n')),
]

# Las URLs públicas llevan el prefijo del idioma: /es/... y /en/...
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('appSaludMentalJoven.urls')),
)
