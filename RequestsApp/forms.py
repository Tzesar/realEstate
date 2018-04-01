from django.forms import ModelForm

from RequestsApp.models import Request


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['full_name', 'email', 'phone_number']
