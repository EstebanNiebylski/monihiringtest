from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class Loan(models.Model):
    class States(models.TextChoices):
        APPROVED = 'OK', _('Approved')
        REJECTED = 'NO', _('Rejected')

    amount = models.FloatField(null=False, default=0)
    state = models.CharField(max_length=2, choices=States.choices, null=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)

