from fastapi import FastAPI
from controller import user
from fastapi.middleware.cors import CORSMiddleware
import redis
import os

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

