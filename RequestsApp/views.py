from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from RequestsApp.models import Usuario
from .forms import ConsultaForm, UsuarioForm


def get_cleaned_user(user_form: UsuarioForm):
    usuario_cleaned = user_form.cleaned_data

    user_list = Usuario.objects.filter(
        nombre_completo__iexact=usuario_cleaned.get("nombre_completo"),
        email__iexact=usuario_cleaned.get("email")
    )

    if user_list.exists():
        return user_list.first()
    else:
        user = user_form.save(commit=False)
        user.email = user.email.lower()

        return user_form.save()


def save_consultas(request):
    if request.method == 'POST':
        consulta_form = ConsultaForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if consulta_form.is_valid() & usuario_form.is_valid():
            usuario = get_cleaned_user(usuario_form)

            consulta = consulta_form.save(commit=False)
            consulta.usuario = usuario

            consulta.save()

            messages.success(request, 'Consulta enviada')
            return HttpResponseRedirect('')

    else:
        consulta_form = ConsultaForm()
        usuario_form = UsuarioForm()

        return render(request, 'requestForm.html', {
        'consulta_form': consulta_form,
        'usuario_form': usuario_form
    })
