from django.urls import path
from . import views

app_name = 'appSaludMentalJoven'

urlpatterns = [
    path('', views.index, name='index'),
]
