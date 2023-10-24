# Model for performance analytics
from pydantic import BaseModel


class Performance(BaseModel):
    user_id: int
    total_trades: int
    total_balance: float
    profit: float
