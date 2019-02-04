from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.fields import AutoSlugField

from .managers import UserManager


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre')
    email = models.EmailField(max_length=40, unique=True, verbose_name='email')
    first_name = None
    username = None
    last_name = None
    slug = AutoSlugField(populate_from=['name'])
    identification = models.CharField(max_length=100, null=True, blank=True, verbose_name='identificacion')
    location = models.TextField(max_length=500, null=True, blank=True, verbose_name='direccion')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['-name', '-email', ]

    def __str__(self):
        return self.name
