from django.db import models


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
