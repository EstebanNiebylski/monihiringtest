from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Requester


class Loan(models.Model):
    class States(models.TextChoices):
        APPROVED = 'OK', _('Approved')
        REJECTED = 'NO', _('Rejected')

    amount = models.FloatField(null=False, default=0)
    state = models.CharField(max_length=2, choices=States.choices, null=True)
    requester = models.ForeignKey(Requester, on_delete=models.CASCADE)

