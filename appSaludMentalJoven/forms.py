from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Inscripcion


class InscripcionForm(forms.ModelForm):
    """Formulario público basado en el modelo Inscripcion (ModelForm)."""

    class Meta:
        model = Inscripcion
        fields = ['nombre', 'email', 'edad', 'comentario']
        labels = {
            'nombre': _('Nombre'),
            'email': _('Email'),
            'edad': _('Edad'),
            'comentario': _('Comentario (opcional)'),
        }
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, actividad=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.actividad = actividad

    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad < 12 or edad > 30:
            raise forms.ValidationError(_('Las actividades están pensadas para personas de 12 a 30 años.'))
        return edad

    def clean(self):
        cleaned = super().clean()
        if self.actividad is not None:
            if self.actividad.finalizada:
                raise forms.ValidationError(_('Esta actividad ya se ha celebrado.'))
            email = cleaned.get('email')
            if email and self.actividad.inscripciones.filter(email__iexact=email).exists():
                raise forms.ValidationError(_('Ya existe una inscripción con ese email en esta actividad.'))
            if self.actividad.plazas_libres <= 0:
                raise forms.ValidationError(_('No quedan plazas libres en esta actividad.'))
        return cleaned
