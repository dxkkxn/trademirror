# Controller for wallet operations
from pydantic import BaseModel


class Wallet(BaseModel):
    wallet_id: int
    user_id: int
    balance: float
