from fastapi import FastAPI, Response, status
from controller import user
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import os
import json

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


class ReplicateWallet(BaseModel):
    wallet_id: str


class AddFiatRequest(BaseModel):
    amount: float


class WithdrawFiatRequest(BaseModel):
    amount: float


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
async def get_latest_transactions(response: Response):
    try:
        ftw = redis_db.lrange("frequent-trading-wallets", 0, 10)
        transactions = []
        for wallet in ftw:
            last_transactions = redis_db.lrange(wallet + ":op", 0, -1)
            for tx in last_transactions:
                transaction = json.loads(tx)
                current_balance = int(str(redis_db.hget(wallet, "balance")))
                previous_balance = int(transaction["current_balance"])
                btc_price = float(transaction["btc_price"])

                if previous_balance == 0:
                    if current_balance > 0:
                        update_percentage = float("inf")
                    elif current_balance < 0:
                        update_percentage = float("-inf")
                    else:
                        update_percentage = 0
                else:
                    update_percentage = (
                        current_balance - previous_balance
                    ) / previous_balance

                transactions.append(
                    {
                        "wallet": wallet,
                        "current_balance": current_balance,
                        "balance_update": ("+" if update_percentage >= 0 else "")
                        + str(update_percentage * 100)
                        + "%",
                        "btc_price": btc_price,
                    }
                )

        response.status_code = status.HTTP_200_OK
        return json.dumps(transactions)
    except:
        raise Exception("Failed at getting latest transactions")


@app.get("/api/user_balance")
async def get_user_balance(response: Response):
    try:
        user_balance = json.loads(
            str(redis_db.hget("users:user-balance", "default_user"))
        )
        fiat_balance = user_balance["fiat"]
        bitcoin_balance = user_balance["btc"]

        response.status_code = status.HTTP_200_OK
        return json.dumps({"fiat": fiat_balance, "btc": bitcoin_balance})
    except:
        raise Exception("Failed at fetching user balance")


@app.get("/api/user_history")
async def get_user_history(response: Response):
    try:
        parsed_transactions = []
        user_transactions = redis_db.lrange(
            "users:transactions:" + "default_user", 0, -1
        )
        for tx in user_transactions:
            transaction = json.loads(tx)

            operation = str(transaction["op"])
            amount = float(transaction["value"])
            previous_balance = int(transaction["current_balance"])
            btc_price = float(transaction["btc_price"])

            parsed_transactions.append(
                {
                    "op": operation,
                    "previous_balance": previous_balance,
                    "btc_price": btc_price,
                    "amount": amount,
                }
            )

        response.status_code = status.HTTP_200_OK
        return json.dumps(parsed_transactions)
    except:
        raise Exception("Failed at fetching user balance")


@app.post("/api/follow_wallet")
async def follow_wallet(data: ReplicateWallet, response: Response):
    try:
        redis_db.rpush("users:tracking:default_user", data.wallet_id)
        message = f"default_user is now tracking {data.wallet_id}"

        response.status_code = status.HTTP_202_ACCEPTED
        return message
    except:
        raise Exception("Failed at adding wallet to the tracking list of default_user")


@app.post("/api/add_fiat")
async def add_fiat(data: AddFiatRequest, response: Response):
    try:
        if data.amount > 0:
            user_balance = json.loads(
                str(redis_db.hget("users:user-balance", "default_user"))
            )
            fiat_balance = int(user_balance["fiat"]) + data.amount
            new_balance = json.dumps({"fiat": fiat_balance, "btc": user_balance["btc"]})
            redis_db.hset("users:user-balance", "default_user", new_balance)

            response.status_code = status.HTTP_202_ACCEPTED
            return new_balance

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Deposit amount is invalid (${data.amount})!"
    except:
        raise Exception("Failed at adding fiat funds to default_user")


@app.post("/api/withdraw_fiat")
async def withdraw_fiat(data: WithdrawFiatRequest, response: Response):
    try:
        if data.amount > 0:
            user_balance = json.loads(
                str(redis_db.hget("users:user-balance", "default_user"))
            )
            fiat_balance = int(user_balance["fiat"])

            if fiat_balance >= data.amount:
                fiat_balance = fiat_balance - data.amount

            new_balance = json.dumps(
                {
                    "fiat": fiat_balance,
                    "btc": user_balance["btc"],
                }
            )
            redis_db.hset("users:user-balance", "default_user", new_balance)

            response.status_code = status.HTTP_202_ACCEPTED
            return new_balance

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Withdraw amount is invalid (${data.amount})!"
    except:
        raise Exception("Failed at adding fiat funds to default_user")
