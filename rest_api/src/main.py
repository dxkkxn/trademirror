from fastapi import FastAPI, HTTPException
from models import User  # Assuming you have a User model defined in "models.py"
import os
import mysql.connector
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allowed_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create a MySQL connection pool instead of a single connection and cursor
mydb = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    user="root",
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
)


# Define a route for creating a user
@app.post("/api/user")
def create_user(user: User):
    print("entreee")
    try:
        cursor = mydb.cursor()
        query = "INSERT INTO users (name, secret) VALUES (%s, %s)"
        values = (user.name, user.secret)
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()
        return {"message": f"{user.name} was registered"}
    except Exception as e:
        return {"error": str(e)}


# Define a route for reading users
@app.get("/api/user")
def read_users():
    try:
        cursor = mydb.cursor(
            dictionary=True
        )  # Use a dictionary cursor for easier result processing
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        cursor.close()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}


# Define a route for deleting a user by ID
@app.delete("/api/user/{user_id}")
def delete_user(user_id: int):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            mydb.commit()
            cursor.close()
            return {"message": f"User with ID {user_id} has been deleted"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print(
        f"{os.environ.get('MYSQL_HOST')}\n{os.environ.get('MYSQL_PASSWORD')}\n{os.environ.get('MYSQL_DATABASE')}"
    )
    config = uvicorn.Config("main:app", port=5000, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
