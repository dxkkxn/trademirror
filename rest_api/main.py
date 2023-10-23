from fastapi import FastAPI
from decouple import config
import redis
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allowed_origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allowed_origins=allowed_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Initialize a Redis connection
redis_host = config("REDIS_HOST")
redis_port = config("REDIS_PORT")
redis_database = config("REDIS_DATABASE")
# redis_client = redis.Redis(host=redis_host, port=5555, db=0)
redis_client = redis.Redis(host=redis_host, port=redis_port or 6379, db= redis_database or 0 )


@app.get("/")
async def get_redis_keys():
    print("hola")
    try:
        # Retrieve all keys from the Redis database
        keys = redis_client.keys("*")
        keys = [key.decode("utf-8") for key in keys]

        # Convert the list of keys to JSON format
        keys_json = json.dumps(keys)

        # Return the JSON response
        return {"keys": keys_json}
    except Exception as e:
        return {"error": str(e)}
