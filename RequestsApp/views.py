import datetime

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
    date_now = datetime.date.today()
    timedelta = datetime.timedelta(weeks=1)
    date_a_week_ago = date_now - timedelta

    consultas = Consulta.objects.filter(fecha__range=(date_a_week_ago, date_now))

    date_now_str = date_now.strftime("%d/%m/%Y")
    date_a_week_ago_str = date_a_week_ago.strftime("%d/%m/%Y")
    message = EmailMessage(
        'Resumen de consultas (%s - %s)' % (date_now_str, date_a_week_ago_str),
        'Las consultas realizadas desde %s hasta %s se adjuntan en el siguiente archivo' % (
            date_now_str, date_a_week_ago_str
        ),
        settings.FROM_EMAIL,
        [settings.TO_EMAIL],
        connection=get_connection(),
    )

    excel_file = ExcelResponse(consultas)
    if consultas.count() > 0:
        message.attach(
            'reporte-%s-%s.xls' % (date_now_str, date_a_week_ago_str),
            excel_file.content,
            'application/vnd.ms-excel'
        )
    else:
        message.body = 'No existen nuevas consultas desde %s hasta %s' % (date_now_str, date_a_week_ago_str)

    message.send()

    return HttpResponseRedirect('/request-form/')
