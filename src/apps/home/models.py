from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.fields import AutoSlugField


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre')
    email = models.EmailField(max_length=40, unique=True, verbose_name='email')
    first_name = None
    username = None
    last_name = None
    slug = AutoSlugField(populate_from=['name'])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['-name', '-email', ]

        # Indexes to make faster calls to the DB
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
        ]

    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

    def get_full_name(self):
        return self.name