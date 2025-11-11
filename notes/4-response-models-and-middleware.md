

---

# 🧭 **`Day 5: Response Models & Middleware in FastAPI`**

---

## 🎯 Learning Objectives

By the end of this lesson, you’ll be able to:

✅ Define and use **response models** to control API output
✅ Use **response_class** to customize output format
✅ Add **custom middleware** for logging requests
✅ Build a **Mini “Quotes API”** (GET + POST) with full validation

---

# 🧩 Part 1: Response Models

## 📘 Definition

A **Response Model** in FastAPI is a **Pydantic model** used to:

* Control **what data is returned** to the client.
* Automatically **filter out unwanted fields**.
* Provide **clear documentation** in Swagger UI.

---

## 💡 Why Response Models Are Useful

Imagine your internal database has sensitive info like `password`, but you only want to return `username` and `email`.
Instead of manually filtering, you use `response_model`.

---

## 🧠 Syntax

```python
@app.get("/items", response_model=ItemOut)
async def get_items():
    return item_data
```

Where:

* `ItemOut` → a **Pydantic model** defining what fields to include in response.
* FastAPI will automatically:

  * Validate output type
  * Serialize to JSON

---

## ⚙️ Example: Student Model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input Model
class StudentIn(BaseModel):
    name: str
    age: int
    grade: str
    password: str  # sensitive info

# Response Model
class StudentOut(BaseModel):
    name: str
    age: int
    grade: str

@app.post("/student", response_model=StudentOut)
async def create_student(student: StudentIn):
    # pretend saving student
    return student
```

### ▶️ Output Example

**Request Body**

```json
{
  "name": "Ayesha",
  "age": 10,
  "grade": "A",
  "password": "1234"
}
```

**Response**

```json
{
  "name": "Ayesha",
  "age": 10,
  "grade": "A"
}
```

🧩 Notice: `password` is not included in the response — **auto-filtered by response_model**.

---

# 🧱 Part 2: Response Class

## 📘 Definition

The `response_class` parameter allows you to control **how the response is returned**, e.g.:

| Class               | Description             |
| ------------------- | ----------------------- |
| `JSONResponse`      | (Default) Returns JSON  |
| `PlainTextResponse` | Returns plain text      |
| `HTMLResponse`      | Returns HTML            |
| `FileResponse`      | Returns a file download |

---

## 🧠 Example

```python
from fastapi.responses import PlainTextResponse, HTMLResponse

@app.get("/plain", response_class=PlainTextResponse)
async def plain():
    return "This is plain text"

@app.get("/html", response_class=HTMLResponse)
async def html():
    return "<h1>Hello, FastAPI!</h1>"
```

---

# 🧩 Part 3: Middleware

## 📘 Definition

**Middleware** is code that runs **before and after each request**.
It’s useful for:

* Logging
* Authentication
* Modifying requests/responses
* Measuring performance

---

## 🧠 Syntax

```python
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # Code before request
    response = await call_next(request)
    # Code after response
    return response
```

---

## ⚙️ Example: Log Requests

```python
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round(time.time() - start_time, 3)
    print(f"📢 {request.method} {request.url} completed in {duration}s")
    return response
```

---

# 🚀 Project: Mini “Quotes API” with GET/POST + Validation

## 🏗️ Objective

Create a small **Quotes API** with:

* `/quotes` (GET): Fetch all quotes
* `/quotes` (POST): Add new quote
* Custom **middleware** to log requests
* Response model for clean output

---

## 🧩 Full Working Code

**`main.py`**

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time

app = FastAPI(title="🌟 Quotes API", version="1.0")

# ----------------------------
# ✅ Pydantic Models
# ----------------------------

class QuoteIn(BaseModel):
    author: str
    text: str

class QuoteOut(BaseModel):
    id: int
    author: str
    text: str

# In-memory database
quotes_db = [
    {"id": 1, "author": "Albert Einstein", "text": "Life is like riding a bicycle. To keep your balance you must keep moving."},
    {"id": 2, "author": "Steve Jobs", "text": "Stay hungry, stay foolish."}
]

# ----------------------------
# ✅ Middleware: Request Logger
# ----------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start, 3)
    print(f"📘 {request.method} {request.url} completed in {process_time}s")
    return response

# ----------------------------
# ✅ GET All Quotes
# ----------------------------

@app.get("/quotes", response_model=list[QuoteOut])
async def get_quotes():
    return quotes_db

# ----------------------------
# ✅ POST Add New Quote
# ----------------------------

@app.post("/quotes", response_model=QuoteOut)
async def add_quote(quote: QuoteIn):
    new_id = len(quotes_db) + 1
    new_quote = {"id": new_id, **quote.dict()}
    quotes_db.append(new_quote)
    return new_quote

# ----------------------------
# ✅ Custom Error Handling
# ----------------------------

@app.exception_handler(HTTPException)
async def custom_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "path": str(request.url)
        }
    )
```

---

## 🧪 Run the App

```bash
uvicorn main:app --reload
```

---

## 🌐 Test Routes

### ✅ 1. GET /quotes

**URL:**
`http://127.0.0.1:8000/quotes`

**Response:**

```json
[
  {
    "id": 1,
    "author": "Albert Einstein",
    "text": "Life is like riding a bicycle. To keep your balance you must keep moving."
  },
  {
    "id": 2,
    "author": "Steve Jobs",
    "text": "Stay hungry, stay foolish."
  }
]
```

---

### ✅ 2. POST /quotes

**Request Body:**

```json
{
  "author": "Rumi",
  "text": "What you seek is seeking you."
}
```

**Response:**

```json
{
  "id": 3,
  "author": "Rumi",
  "text": "What you seek is seeking you."
}
```

---

### 🪄 Terminal Output (Middleware)

```
📘 GET http://127.0.0.1:8000/quotes completed in 0.002s
📘 POST http://127.0.0.1:8000/quotes completed in 0.003s
```

---

# 🧩 Summary Table

| Concept                | Description                              | Example                       |
| ---------------------- | ---------------------------------------- | ----------------------------- |
| **response_model**     | Controls which fields appear in response | `response_model=QuoteOut`     |
| **response_class**     | Changes how the response is formatted    | `response_class=HTMLResponse` |
| **middleware**         | Runs before/after each request           | Logging, authentication       |
| **call_next(request)** | Passes control to next layer             | Executes the next handler     |

---

# 🧭 Next Steps (Day 6 Preview)

Tomorrow, you’ll learn:

**Day 6: Routers & Modular Apps**

* `APIRouter`
* Organize your app into modules
* Build clean project folder structure (e.g., `routers/quotes.py`, `models/quote_model.py`)

---

