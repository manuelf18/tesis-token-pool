from apps.tokens.models import Pool
from apps.tokens.contract import PoolContract

pools = Pool.objets.all()
pool_contract = PoolContract()

for pool in pools:
    pool_contract.create_pool(pool.name, pool.token_name)
