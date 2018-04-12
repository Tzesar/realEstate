from django.forms import ModelForm

from RequestsApp.models import Consulta, Usuario


class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        exclude = ['fecha']
        localized_fields = '__all__'


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        localized_fields = '__all__'
