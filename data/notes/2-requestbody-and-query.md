Perfect 🔥 Asadullah — welcome to **Day 3** of your **AI Engineer FastAPI Roadmap**.
Today, you’ll learn one of the most **important backend skills** for any AI system:
👉 how to **send and validate data** to your API using **path parameters**, **query parameters**, and **request bodies**.

Let’s go step-by-step — with **definitions**, **syntax**, and **hands-on examples** (AI-style 🧠).

---

# 🧩 Day 3: Request Body & Query Parameters

---

## 🎯 Learning Goals

By the end of today, you’ll be able to:

✅ Define **path**, **query**, **body**, and **form** inputs
✅ Use **Pydantic BaseModel** for input validation
✅ Build a `/predict` API endpoint that accepts **JSON data**
✅ Understand how data flows from **client → FastAPI → Python function**

---

## ⚙️ 1. FastAPI Parameter Types Overview

When a client sends a request to your API, the data can come from different places:

| Type                | Example                    | Where it appears | Use Case                          |
| ------------------- | -------------------------- | ---------------- | --------------------------------- |
| **Path Parameter**  | `/user/123`                | Inside URL       | Identify resource (e.g., user ID) |
| **Query Parameter** | `/user?id=123&active=true` | After `?` in URL | Filter, search, pagination        |
| **Body Parameter**  | JSON data in POST request  | Request body     | Submit form data, ML input        |
| **Form Parameter**  | Sent via HTML forms        | Form body        | Login forms, uploads              |

---

# 🧱 2. Path Parameters

### 🧠 Definition:

Path parameters are **dynamic parts of the URL** that you define inside curly braces `{}`.

### 🧩 Syntax:

```python
@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 🧪 Example Run:

Request:

```
GET http://127.0.0.1:8000/user/42
```

Response:

```json
{"user_id": 42}
```

---

# 🔍 3. Query Parameters

### 🧠 Definition:

Query parameters come **after the `?`** in the URL and are used for optional filters or settings.

### 🧩 Syntax:

```python
@app.get("/search")
def search_users(name: str, active: bool = True):
    return {"name": name, "active": active}
```

### 🧪 Example Run:

Request:

```
GET http://127.0.0.1:8000/search?name=Asad&active=true
```

Response:

```json
{"name": "Asad", "active": true}
```

---

# 📦 4. Request Body (JSON Input)

### 🧠 Definition:

The **request body** holds JSON data sent by the client — typically used in `POST` or `PUT` requests.

### 🧩 Syntax using Pydantic:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define data structure
class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/create_user")
def create_user(user: User):
    return {"message": "User created successfully!", "data": user}
```

### 🧪 Example JSON Input:

```json
{
  "name": "Asad",
  "age": 25,
  "email": "asad@example.com"
}
```

### 🧠 FastAPI automatically:

✅ Validates types (e.g., `age` must be `int`)
✅ Converts JSON → Python object
✅ Returns Python dict → JSON response

---

# 🧾 5. Form Inputs (Optional Bonus)

When you’re receiving data from HTML `<form>` submissions:

```python
from fastapi import Form

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

---

# 🤖 6. Practice Task — `/predict` Endpoint

Now let’s make it practical — a **mini AI-style endpoint**.

You’ll create `/predict` that takes JSON input (like an ML model would) and returns a mock prediction.

---

### 🧩 Full Code Example — `main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel

# Step 1: Initialize app
app = FastAPI(title="Day 3 - Request Body & Parameters")

# Step 2: Define Pydantic model for input validation
class PredictionInput(BaseModel):
    age: int
    income: float

# Step 3: Define route with body input
@app.post("/predict")
def predict(data: PredictionInput, verbose: bool = False):
    """
    Example /predict API that mimics ML model prediction
    Body: {"age": 25, "income": 50000}
    Query Param: verbose=true
    """
    # Simple logic for demo
    if data.income > 40000 and data.age < 30:
        prediction = "Likely to buy AI course 🚀"
    else:
        prediction = "Not likely to buy right now ❌"

    # If user added ?verbose=true in URL
    if verbose:
        return {
            "input": data.dict(),
            "prediction": prediction,
            "confidence": "0.87"
        }

    return {"prediction": prediction}

# Example: POST http://127.0.0.1:8000/predict?verbose=true
# Body:
# {
#   "age": 25,
#   "income": 50000
# }
```

---

### 🧪 How to Test

Run your app:

```bash
uvicorn main:app --reload
```

Then open your browser and go to:
👉 `http://127.0.0.1:8000/docs`

Try this:

```json
{
  "age": 25,
  "income": 50000
}
```

Response:

```json
{
  "input": {"age": 25, "income": 50000},
  "prediction": "Likely to buy AI course 🚀",
  "confidence": "0.87"
}
```

---

# 🧠 Summary Table

| Concept             | Location        | Example URL         | Python Example               | Method |
| ------------------- | --------------- | ------------------- | ---------------------------- | ------ |
| **Path Parameter**  | URL segment     | `/user/10`          | `def get_user(id: int)`      | `GET`  |
| **Query Parameter** | After `?`       | `/search?name=Asad` | `def search(name: str)`      | `GET`  |
| **Request Body**    | JSON payload    | POST with JSON      | `def predict(data: Model)`   | `POST` |
| **Form Data**       | Form submission | `/login`            | `def login(user: Form(...))` | `POST` |

---

# 🧩 Homework for Day 3

1️⃣ Add another field to your `/predict` model → `"education": "BSCS"`
2️⃣ Add logic that changes prediction based on education
3️⃣ Test both `verbose=true` and `verbose=false`

---

