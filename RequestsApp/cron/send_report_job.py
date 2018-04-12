import datetime

from django.core.mail import EmailMessage, get_connection
from excel_response import ExcelResponse

from RealEstate import settings
from RequestsApp.models import Consulta, Reporte


def process_queryset(consultas):
    data = [
        [
            'nombre_completo', 'email', 'nro_telefono', 'ocupacion', 'nacionalidad', 'idioma',
            'interes', 'rubro', 'otro_rubro', 'zona_preferencia', 'tamaño', 'presupuesto', 'formacion'
        ]
    ]

    for c in consultas:
        u = c.usuario
        row = [
            u.nombre_completo, u.email, u.nro_telefono, u.ocupacion, u.nacionalidad, u.idioma,
            c.interes, c.rubro, c.otro_rubro, c.zona_preferencia, c.tamanho, c.presupuesto, c.formacion
        ]

        data.append(row)

    return data


def send_email():
    date_now = datetime.date.today()
    timedelta = datetime.timedelta(weeks=1)
    date_a_week_ago = date_now - timedelta

    last_report = Reporte.objects.last()

    if last_report is None or last_report.fecha_ejecucion < date_a_week_ago:
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

        excel_file = ExcelResponse(process_queryset(consultas))
        if consultas.count() > 0:
            message.attach(
                'reporte-%s-%s.xls' % (date_now_str, date_a_week_ago_str),
                excel_file.content,
                'application/vnd.ms-excel'
            )
        else:
            message.body = 'No existen nuevas consultas desde %s hasta %s' % (date_now_str, date_a_week_ago_str)

        message.send()

        Reporte(cantidad_consultas=consultas.count()).save()

