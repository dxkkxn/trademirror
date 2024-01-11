@app.get("/api/latest_transactions")
async def get_latest_transactions():
    try:
        ftw = redis_db.lrange("frequent-trading-wallets", 0, 10)
        transactions = {}
        for wallet in ftw:
            last_transaction = redis_db.lrange(wallet + ":op", 0, 0)
            for tx in last_transaction:
                transactions = []
                transaction = json.loads(tx)
                current_balance = int(str(redis_db.hget(wallet, "balance")))
                previous_balance = int(transaction["current_balance"])
                btc_price = float(transaction["btc_price"])
                update_percentage = (
                    current_balance - previous_balance
                ) / previous_balance
                transactions.append({
                    "wallet": wallet,
                    "current_balance": current_balance,
                    "balance_update": ("+" if update_percentage >= 0 else "-")
                    + str(update_percentage * 100)
                    + "%",
                    "btc_price": btc_price,
                })
        return json.dumps(transactions)
    except:
        raise Exception("Failed at getting latest transactions")
