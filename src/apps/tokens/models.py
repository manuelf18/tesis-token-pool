from django.db import models
from django.utils import timezone

from ..core.models import AbstractHistory
from ..profiles.models import User
from .signals import PoolSignals
from .contracts import TokenContract


class TokenType(AbstractHistory):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True,
                            default='', verbose_name="Nombre")

    address = models.CharField(max_length=100, null=True, blank=True, unique=True,
                               default='', verbose_name="Nombre")

    def save(self, *args, **kwargs):
        try:
            tc = TokenContract(self.name)
            self.address = tc.address
            super().save(self, *args, **kwargs)
        except Exception as e:
            print('hubo un error {}'.format(e))


class Pool(PoolSignals, AbstractHistory):
    name = models.CharField(max_length=50, null=True, blank=True,
                            default='', verbose_name="Nombre")
    token_type = models.ForeignKey(TokenType, null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now,
                                      verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name='Fecha de finalizacion')
    token_value = models.IntegerField(default=1, verbose_name='Valor del Token')
    admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    closed = models.BooleanField(default=False, verbose_name='Cerrada')

    @classmethod
    def send_to_contract(cls):
        from .contracts import PoolContract
        pools = cls.objects.filter(closed=False)
        pc = PoolContract()
        for pool in pools:
            pc.create_pool(pool.name, pool.token_type.name, pool.token_value)


class Network(AbstractHistory):
    url = models.CharField(max_length=50, null=True, blank=True,
                           default='', verbose_name="Url")
    port = models.CharField(max_length=50, null=True, blank=True,
                            default='', verbose_name="Puerto")
    connected = models.BooleanField(default=False, verbose_name='Conectado')


class Transaction(AbstractHistory):
    DEPOSIT = 0
    WITHDRAW = 1

    CHOICES = [(DEPOSIT, 0), (WITHDRAW, 1)]

    address = models.CharField(max_length=50, default='', verbose_name='Dirección')
    transaction_type = models.IntegerField(choices=CHOICES)
    amount = models.DecimalField(verbose_name='Cantidad de tokens', max_digits=9, decimal_places=4)
    value = models.DecimalField(verbose_name='Valor de los tokens', max_digits=9, decimal_places=4)
