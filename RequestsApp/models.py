from django.db import models

BUDGET_CHOICES = (
    ('0-1.000.000', '0 - 1.000.000 USD'),
    ('1.000.000-3.000.000', '1.000.000 - 3.000.000 USD'),
    ('3.000.000-6.000.000', '3.000.000 - 6.000.000 USD')
)

CITY_CHOICES = (
    ('San Lorenzo', 'San Lorenzo'),
    ('Fernando de la Mora', 'Fernando de la Mora'),
    ('Asuncion', 'Asuncion')
)

COUNTRY_CHOICES = (
    ('PRY', 'Paraguay'),
    ('BRZ', 'Brazil'),
    ('ARG', 'Argentina')
)

ACTIVITY_TYPE_CHOICES = (
    ('reforestacion', 'Reforestacion'),
    ('cuenca_acuifera', 'Cuenca Acuifera'),
    ('otros', 'Otros')
)

PREFERENCE_ZONE_CHOICES = (
    ('oriental', 'Oriental'),
    ('occidental', 'Occidental'),
    ('otras_sugerencias', 'Otras sugerencias')
)

SIZE_CHOICES = (
    ('1-500', '1 - 500 Hect.'),
    ('500-1000', '500 - 1000 Hect.'),
    ('1000-3000', '1000 - 3000 Hect.')
)


class Pais(models.Model):
    nombre = models.CharField(max_length=20)


class Request(models.Model):
    full_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, verbose_name="Pais del lote")
    company_name = models.CharField(max_length=20)
    job_title = models.CharField(max_length=20)

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    preference_zone = models.CharField(max_length=20, choices=PREFERENCE_ZONE_CHOICES)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    budget = models.CharField(max_length=30, choices=BUDGET_CHOICES)

