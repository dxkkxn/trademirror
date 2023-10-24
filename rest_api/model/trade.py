# Controller for trade operations
from pydantic import BaseModel


class Trade(BaseModel):
    trade_id: int
    user_id: int
    trade_type: str
    amount: float
    date: str
