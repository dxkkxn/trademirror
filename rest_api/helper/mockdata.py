import redis
import random
from decouple import config
from pydantic import BaseModel
import sys
import os

# Add the parent directory (project root) to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from model.user import User
from model.trade import Trade
from model.wallet import Wallet
from model.performance import Performance


redis_host = config("REDIS_HOST")
redis_port = config("REDIS_PORT")
redis_database = config("REDIS_DATABASE")
# Connect to your Redis server
redis_client = redis.Redis(
    host=redis_host, port=redis_port or 6379, db=redis_database or 0
)
# Generate sample user data
sample_users = [
    User(id=i, username=f"user{i}", password=f"password{i}") for i in range(1, 26)
]

# Generate sample trade data
sample_trades = [
    Trade(
        trade_id=i,
        user_id=random.randint(1, 26),
        trade_type=random.choice(["buy", "sell"]),
        amount=round(random.uniform(10.0, 1000.0), 2),
        date=f"2023-01-{i % 30 + 1:02d}",
    )
    for i in range(1, 26)
]

# Generate sample wallet data
sample_wallets = [
    Wallet(
        wallet_id=i,
        user_id=random.randint(1, 26),
        balance=round(random.uniform(100.0, 10000.0), 2),
    )
    for i in range(1, 26)
]

# Generate sample performance data
sample_performances = [
    Performance(
        user_id=i,
        total_trades=random.randint(1, 100),
        total_balance=round(random.uniform(100.0, 10000.0), 2),
        profit=round(random.uniform(-1000.0, 1000.0), 2),
    )
    for i in range(1, 26)
]

# Set the data in Redis
for user in sample_users:
    redis_client.hmset(f"user:{user.id}", user.dict())

for trade in sample_trades:
    redis_client.hmset(f"trade:{trade.trade_id}", trade.dict())

for wallet in sample_wallets:
    redis_client.hmset(f"wallet:{wallet.wallet_id}", wallet.dict())

for performance in sample_performances:
    redis_client.hmset(f"performance:{performance.user_id}", performance.dict())
