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
    today = datetime.date.today()
    timedelta = datetime.timedelta(days=1)
    yesterday = today - timedelta

    last_report = Reporte.objects.last()

    # This check was done to make the request report a daily report
    # if last_report is None or last_report.fecha_ejecucion < yesterday:
    consultas = Consulta.objects.all()

    today_str = today.strftime("%d/%m/%Y")
    message = EmailMessage(
        'Resumen de consultas (%s)' % today_str,
        'Las consultas realizadas hasta %s se adjuntan en el siguiente archivo' % today_str,
        settings.FROM_EMAIL,
        [settings.TO_EMAIL],
        connection=get_connection(),
    )

    excel_file = ExcelResponse(process_queryset(consultas))
    if consultas.count() > 0:
        message.attach(
            'reporte-%s.xls' % today_str,
            excel_file.content,
            'application/vnd.ms-excel'
        )
    else:
        message.body = 'No existen nuevas consultas hasta %s' % today_str

    message.send()

    Reporte(cantidad_consultas=consultas.count()).save()
