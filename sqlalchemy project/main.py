from fastapi import FastAPI , HTTPException
from database import get_db_connection
from models import create_tables
from contextlib import asynccontextmanager

# create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App is starting up...")
    create_tables()      # ✅ Runs once before the app starts
    yield                # 🕐 Application runs during this period
    print("🛑 App is shutting down...")

app = FastAPI(lifespan=lifespan,title='FastAPI CRUD without ORM')

@app.get('/')
def welcome():
    return {'Name':'Ayan Ahmed','Goal':'AI Engineer'}


# 🟢 Create (POST)
@app.post("/users/")
def create_user(username: str, email: str, full_name: str = None):
    with get_db_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)",
                (username, email, full_name),
            )
            conn.commit()
            return {"message": "User created successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


# 🔵 Read all (GET)
@app.get("/users/")
def read_users():
    with get_db_connection() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
        return [dict(user) for user in users]
    

# 🔵 Read single user (GET)
@app.get("/users/{user_id}")
def read_user(user_id: int):
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(user)