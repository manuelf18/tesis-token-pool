from django.db import models


class HistoryBase(models.Model):
    """
    An abstract model that allows future audit
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    active = models.BooleanField(verbose_name='activo', default=True)

    class Meta:
        abstract = True

    @property
    def is_active(self, *args, **kwargs):
        return self.active
