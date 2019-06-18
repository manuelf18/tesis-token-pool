from django.db import models
from django.utils import timezone

from ..core.models import AbstractHistory
from ..profiles.models import User


class Pool(AbstractHistory):
    name = models.CharField(max_length=50, null=True, blank=True,
                            default='', verbose_name="Nombre")
    token_name = models.CharField(max_length=50, null=True, blank=True,
                                  default='', verbose_name="Nombre del Token")
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now,
                                      verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name='Fecha de finalizacion')
    token_value = models.IntegerField(default=1, verbose_name='Valor del Token')
    admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class Network(AbstractHistory):
    url = models.CharField(max_length=50, null=True, blank=True,
                           default='', verbose_name="Url")
    port = models.CharField(max_length=50, null=True, blank=True,
                            default='', verbose_name="Puerto")
    connected = models.BooleanField(default=False, verbose_name='Conectado')
