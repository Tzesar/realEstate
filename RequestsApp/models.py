from django.db import models

from django.utils.translation import gettext_lazy as _

BUDGET_CHOICES = (
    ('0-10.000', '0 - 10.000 USD'),
    ('10.000-20.000', '10.000 USD - 20.000 USD'),
    ('20.000-50.000', '20.000 USD - 50.000 USD'),
    ('50.000-100.000', '50.000 USD - 100.000 USD'),
    ('100.000-150.000', '100.000 USD - 150.000 USD'),
    ('150.000-200.000', '150.000 USD - 200.000 USD'),
    ('200.000-350.000', '200.000 USD - 350.000 USD'),
    ('350.000-500.000', '350.000 USD - 500.000 USD'),
    ('500.000-800.000', '500.000 USD - 800.000 USD'),
    ('800.000-1.500.000', '800.000 USD - 1.500.000 USD'),
    ('1.500.000-3.000.000', '1.500.000 USD - 3.000.000 USD'),
    ('3.000.000-8.000.000', '3.000.000 - 8.000.000 USD'),
    ('8.000.000-*', 'Mayor a 8.000.000 USD')
)

ACTION_CHOICES = (
    ('venta', 'Venta'),
    ('compra', 'Compra'),
    ('alquiler', 'Alquiler'),
    ('remates', 'Remates'),
    ('administracion', 'Administración'),
    ('topografia', 'Topografía'),
    ('asesoramiento', 'Asesoramiento')
)

LANGUAGE_CHOICES = (
    ('español', 'Español'),
    ('inglés', 'Inglés'),
    ('portugués', 'Portugués'),
    ('alemán', 'Alemán'),
    ('francés', 'Francés')
)

ACTIVITY_TYPE_CHOICES = (
    ('ganaderia', 'Ganadería'),
    ('agricultura', 'Agricultura'),
    ('loteamiento', 'Loteamiento'),
    ('inversion_inmobiliaria', 'Inversión Inmobiliaria'),
    ('puerto', 'Puerto'),
    ('cuenca_aquifera', 'Cuenca Acuifera'),
    ('residencias', 'Residencias'),
    ('terrenos', 'Terrenos'),
    ('otros', 'Otros')
)

PREFERENCE_ZONE_CHOICES = (
    ('oriental', 'Oriental'),
    ('occidental', 'Occidental')
)

SIZE_CHOICES = (
    ('0 - 1 m2', '0 - 10.000 m2'),
    ('1 - 2.5 HA', '10.000 m2 - 25.000 m2'),
    ('2.5 - 5 HA', '25.000 m2 (2,5 HA)- 5 HA'),
    ('5 - 10 HA', '5 HA - 10 HA'),
    ('10 - 20 HA', '10 HA - 20 HA'),
    ('20 - 50 HA', '20 HA - 50 HA'),
    ('50 - 100 HA', '50 HA - 100 HA'),
    ('100 - 300 HA', '100 HA - 300 HA'),
    ('300 - 600 HA', '300 HA - 600 HA'),
    ('600 - 2.000 HA', '600 HA - 2.000 HA'),
    ('2.000 - 5.000 HA', '2.000 HA - 5.000 HA'),
    ('5.000 - 10.000 HA', '5.000 HA - 10.000 HA'),
    ('10.000 HA - *', 'Mayor a 10.000 HA')
)

FORMATION_CHOICES = (
    ('formado', 'Formado'),
    ('semi-formado', 'Semi Formado'),
    ('a-formar', 'A Formar')
)


class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=20)
    nacionalidad = models.CharField(max_length=20)
    email = models.EmailField()
    nro_telefono = models.CharField(max_length=20, verbose_name=_('nro. de teléfono'))
    ocupacion = models.CharField(max_length=20, verbose_name=_('ocupación'))
    idioma = models.CharField(max_length=25, choices=LANGUAGE_CHOICES, blank=False, default='español')

    def __str__(self):
        return self.nombre_completo


class Request(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    interes = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True, verbose_name=_('interés'))

    rubro = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES, blank=True)
    otro_rubro = models.CharField(max_length=50, blank=True)

    zona_preferencia = models.CharField(max_length=20, choices=PREFERENCE_ZONE_CHOICES, blank=True,
                                        verbose_name=_('zona de preferencia'))
    # Specify that HA means "Hectárea"
    tamanho = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True, verbose_name=_('tamaño'))
    presupuesto = models.CharField(max_length=30, choices=BUDGET_CHOICES, blank=True)

    formacion = models.CharField(max_length=30, choices=FORMATION_CHOICES, blank=True, verbose_name=_('formación'))

    def __str__(self):
        return self.usuario.__str__() + " interes:" + self.interes

