from fastapi import FastAPI
from controller import user
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
import json

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

app = FastAPI()
redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# allowing cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user", tags=["users"])


@app.get("/api/")
async def check_status():
    return {"API is working"}


@app.get("/api/redis_status")
async def get_redis_status():
    try:
        redis_db.ping()
        return {"Redis is working"}
    except redis.ConnectionError:
        return {"Error Redis not working"}

@app.get("/api/latest_transactions")
async def get_latest_transactions():
    try:
        ftw = redis_db.lrange("frequent-trading-wallets", 0, 0)
        transactions = {}
        for wallet in ftw:
            transactions[wallet] = {}
            last_transaction = redis_db.lrange(wallet + ":op", 0, 0)
            for tx in last_transaction:
                transaction = json.loads(tx)
                current_balance = int(str(redis_db.hget(wallet, "balance")))
                previous_balance = int(transaction["current_balance"])
                btc_price = float(transaction["btc_price"])
                update_percentage = (current_balance - previous_balance) / previous_balance
                transactions[wallet] = {
                    "wallet": wallet,
                    "current_balance": current_balance,
                    "balance_update": ("+" if update_percentage >= 0 else "-") + str(update_percentage * 100) + "%",
                    "btc_price" : btc_price
                }
        return json.dumps(transactions)
    except:
        raise Exception("Failed at getting latest transactions")

@app.get("/api/user_balance")
async def get_user_balance():
    try:
        pass
    except:
        pass

@app.get("/api/user_history")
async def get_user_balance():
    try:
        pass
    except:
        pass

@app.post("/api/follow_wallet")
async def follow_wallet():
    try:
        pass
    except:
        pass