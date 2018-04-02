from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ConsultaForm, UsuarioForm


def get_clean_user(usuario_form):
    return usuario_form.save()


def get_full_name(request):
    if request.method == 'POST':
        consulta_form = ConsultaForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if consulta_form.is_valid() & usuario_form.is_valid():
            consulta = consulta_form.save(commit=False)

            usuario = get_clean_user(usuario_form)

            consulta.usuario = usuario

            consulta.save()
            return HttpResponseRedirect('/thanks/')

    else:
        consulta_form = ConsultaForm()
        usuario_form = UsuarioForm()

    return render(request, 'requestForm.html', {
        'consulta_form': consulta_form,
        'usuario_form' : usuario_form
    })
