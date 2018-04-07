from django.forms import ModelForm

from RequestsApp.models import Request, Usuario


class ConsultaForm(ModelForm):
    class Meta:
        model = Request
        fields = ['interes', 'rubro', 'zona_preferencia', 'tamanho', 'presupuesto', 'formacion']


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'email', 'nro_telefono', 'idioma', 'nacionalidad', 'ocupacion']
