from django.db import models
from django.utils import timezone

from apps.core.models import HistoryBase
from apps.profiles.models import User


class Pool(HistoryBase):
    name = models.CharField(max_length=50, null=True, blank=True,
                            default='', verbose_name="Nombre")
    token_name = models.CharField(max_length=50, null=True, blank=True,
                                  default='', verbose_name="Nombre del Token")
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now,
                                      verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name='Fecha de finalizacion')
    admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


"""
class Token(HistoryBase):
    pool = models.ForeignKey(Pool, null=True, blank=True, related_name='token',
                             on_delete=models.SET_NULL, verbose_name="Tipo de proyecto")
    owner = models.ForeignKey(User, null=True, blank=True, related_name='token',
                              on_delete=models.SET_NULL, verbose_name="Dueño")
"""
