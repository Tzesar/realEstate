from django.contrib import messages
from django.core.mail import get_connection, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from excel_response import ExcelResponse

from RealEstate import settings
from RequestsApp.models import Usuario, Consulta
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


def send_email(request):

    message = EmailMessage(
        'Django Test',
        'This is an email from Django.',
        settings.FROM_EMAIL,
        [settings.TO_EMAIL],
        connection=get_connection(),
    )

    consultas = Consulta.objects.all()
    excel_file = ExcelResponse(consultas)
    if consultas.count() > 0:
        message.attach('report.xls', excel_file.content, 'application/vnd.ms-excel')

    message.send()

    return HttpResponseRedirect('/request-form/')
