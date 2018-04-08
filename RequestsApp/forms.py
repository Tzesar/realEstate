from django.forms import ModelForm

from RequestsApp.models import Request, Usuario


class ConsultaForm(ModelForm):
    class Meta:
        model = Request
        fields = '__all__'
        localized_fields = '__all__'


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        localized_fields = '__all__'
