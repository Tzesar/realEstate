from django.shortcuts import render
from django.http import HttpResponseRedirect

from RequestsApp.models import Usuario
from .forms import ConsultaForm, UsuarioForm


def get_cleaned_user(user_form: UsuarioForm):
    usuario_cleaned = user_form.cleaned_data

    user_list = Usuario.objects.filter(
        nro_telefono=usuario_cleaned.get("nro_telefono"),
        email=usuario_cleaned.get("email")
    )

    if user_list.exists():
        return user_list.first()
    else:
        return user_form.save()


def save_consultas(request):
    if request.method == 'POST':
        consulta_form = ConsultaForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if consulta_form.is_valid() & usuario_form.is_valid():
            consulta = consulta_form.save(commit=False)

            usuario = get_cleaned_user(usuario_form)

            consulta.usuario = usuario

            consulta.save()
            return HttpResponseRedirect('/request-form/')

    else:
        consulta_form = ConsultaForm()
        usuario_form = UsuarioForm()

    return render(request, 'requestForm.html', {
        'consulta_form': consulta_form,
        'usuario_form' : usuario_form
    })
