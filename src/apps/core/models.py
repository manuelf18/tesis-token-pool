from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone

from .managers import BaseManager


def callMethod(o, name, *args, **kwargs):
    """
    Function that calls a method inside of given instance.
    It passes all the arguments and Keyword Arguments to the
    instance.
    """
    getattr(o, name)(*args, **kwargs)


class AbstractHistory(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Fecha de actualización')
    active = models.BooleanField(verbose_name='activo', default=True)
    objects = BaseManager()

    class Meta:
        abstract = True

    @property
    def is_active(self, *args, **kwargs):
        return self.active


class Signals(object):
    """
    pass functions starting with _pre_save to execute them before the save() method of the Models,
    and pass functions starting with _post_save to execute them after the save() method.
    """
    _avoid_signals = settings.AVOID_SIGNALS if settings.AVOID_SIGNALS else False

    def __pre_save_handler(self, instance, *args, **kwargs):
        methods = [_m for _m in dir(self.__class__)
                   if _m.startswith('_pre_save')]
        for m in methods:
            callMethod(self, m, instance, *args, **kwargs)

    def __post_save_handler(self, instance, created, *args, **kwargs):
        methods = [_m for _m in dir(self.__class__)
                   if _m.startswith('_post_save')]
        for m in methods:
            callMethod(self, m, instance, created, *args, **kwargs)

    def save(self, *args, **kwargs):
        if kwargs.get('commit', True) is True:
            instance = self
            created = self.pk is None
            if self._avoid_signals is False:
                self.__pre_save_handler(instance)
            super().save(*args, **kwargs)
            if self._avoid_signals is False:
                self.__post_save_handler(instance, created)
