from apps.tokens.models import Pool
from apps.tokens.contracts import PoolContract

pools = Pool.objects.all()
pool_contract = PoolContract()

for pool in pools:
    pool_contract.create_pool(pool.name, pool.token_name, 1)
