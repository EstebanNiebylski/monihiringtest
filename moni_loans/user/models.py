from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class Genders(models.TextChoices):
        MAN = 'M', _('Male')
        WOMAN = 'F', _('Female')
        OTHER = 'X', _('Not specified')

    dni = models.CharField(
        primary_key=True,
        unique=True,
        max_length=8
    )
    email = models.EmailField(
        null=False,
        max_length=254
    )
    name = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    gender = models.CharField(choices=Genders.choices, max_length=2, null=False)

