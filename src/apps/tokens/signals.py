from ..core.models import Signals
from .contracts import PoolContract


class PoolSignals(Signals):
    def _post_save_add_to_contract(sender, instance, created, *args, **kwargs):
        if created and not instance._avoid_signals:
            pc = PoolContract()
            pc.create_pool(instance.name, instance.token_type.name, instance.token_value)
