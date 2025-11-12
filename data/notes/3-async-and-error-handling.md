
---

# 🧠 **`Day 4: Async & Error Handling in FastAPI`**

---

## 🎯 `Learning Goals`

By the end of this lesson, you will be able to:

✅ Understand and write **async endpoints** in FastAPI
✅ Know **why** async improves performance
✅ Use **HTTPException** for proper error handling
✅ Build a **real endpoint `/divide?x=10&y=0`** that safely handles divide-by-zero errors

---

## ⚙️ 1. What is Async Programming?

### 🧩 **Definition:**

**Asynchronous programming** allows your app to handle multiple requests **concurrently** — without waiting for one to finish before starting another.

👉 It’s like multitasking:
While one request waits for data (like from a database or API), your app can start processing another request.

---

### 🧠 Why Async Matters in FastAPI

| Without `async` (sync code)                | With `async` (async code)                              |
| ------------------------------------------ | ------------------------------------------------------ |
| Each request blocks the server until done. | Requests run concurrently.                             |
| Slower under heavy load.                   | Faster for I/O-heavy apps (APIs, AI calls, databases). |
| Simple to reason about.                    | Requires using `await` for async operations.           |

---

## 💻 2. Syntax: How to Write Async Functions

### Basic Example:

```python
@app.get("/hello")
async def say_hello():
    return {"message": "Hello Async FastAPI!"}
```

### With `await`:

You can only use `await` **inside** `async def` functions:

```python
import asyncio

@app.get("/wait")
async def wait_example():
    await asyncio.sleep(2)
    return {"message": "I waited 2 seconds asynchronously ⏳"}
```

✅ The server won’t freeze — it can handle other users during the wait.

---

# 🚨 3. Error Handling with HTTPException

When something goes wrong (like invalid input or divide by zero), you should send the **right HTTP status code and message**.

---

### 🧩 **Definition:**

`HTTPException` is used in FastAPI to **manually raise an error** that returns:

* A specific HTTP status code
* A custom error message

---

### 🧱 **Syntax:**

```python
from fastapi import HTTPException

@app.get("/error_example")
def error_demo():
    raise HTTPException(
        status_code=400,
        detail="Invalid request data."
    )
```

Response:

```json
{
  "detail": "Invalid request data."
}
```

---

# 🧮 4. Practice Task — `/divide` Endpoint

Let’s build the Day 4 project step-by-step 👇

---

## 🔹 Step 1: Create File `main.py`

```python
from fastapi import FastAPI, HTTPException
import asyncio

# Initialize the app
app = FastAPI(title="Day 4 - Async & Error Handling Demo")

# 🧮 /divide endpoint using async + error handling
@app.get("/divide")
async def divide_numbers(x: float, y: float):
    """
    Asynchronous division endpoint.
    Example: /divide?x=10&y=2
    """

    # Simulate processing delay (like a real ML API)
    await asyncio.sleep(1)

    # Handle invalid input
    if y == 0:
        # Raise an HTTPException if division by zero
        raise HTTPException(
            status_code=400,
            detail="❌ Division by zero is not allowed. Please use a non-zero denominator."
        )

    # Perform division safely
    result = x / y

    # Return structured JSON response
    return {
        "operation": f"{x} ÷ {y}",
        "result": result,
        "message": "✅ Division successful!"
    }
```

---

## 🔹 Step 2: Run the App

In terminal:

```bash
uvicorn main:app --reload
```

Visit in browser:

```
http://127.0.0.1:8000/divide?x=10&y=2
```

✅ Output:

```json
{
  "operation": "10.0 ÷ 2.0",
  "result": 5.0,
  "message": "✅ Division successful!"
}
```

---

## 🔹 Step 3: Try an Error Case

Now visit:

```
http://127.0.0.1:8000/divide?x=10&y=0
```

❌ Output:

```json
{
  "detail": "❌ Division by zero is not allowed. Please use a non-zero denominator."
}
```

FastAPI automatically sets:

```
HTTP/1.1 400 Bad Request
```

---

# 🧠 Explanation of Logic

| Line                       | Code                                                            | Explanation |
| -------------------------- | --------------------------------------------------------------- | ----------- |
| `async def divide_numbers` | Makes the route asynchronous                                    |             |
| `await asyncio.sleep(1)`   | Simulates an async operation (like calling a model or database) |             |
| `if y == 0:`               | Prevents runtime crash due to divide-by-zero                    |             |
| `raise HTTPException(...)` | Gracefully returns error JSON                                   |             |
| `return {...}`             | Returns success result as JSON                                  |             |

---

# 🧩 5. Advanced — Adding a Global Exception Handler (Optional)

If you want **consistent custom error messages** across your entire app 👇

```python
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "hint": "Check your input values again.",
            "path": str(request.url)
        },
    )
```

✅ Output (for divide by zero):

```json
{
  "error": true,
  "message": "❌ Division by zero is not allowed. Please use a non-zero denominator.",
  "hint": "Check your input values again.",
  "path": "http://127.0.0.1:8000/divide?x=10&y=0"
}
```

---

# 🧭 Summary Table

| Concept             | Description                        | Example                              |
| ------------------- | ---------------------------------- | ------------------------------------ |
| **`async def`**     | Allows concurrent request handling | `async def my_route()`               |
| **`await`**         | Waits for async operations         | `await asyncio.sleep(1)`             |
| **`HTTPException`** | Sends controlled error responses   | `raise HTTPException(400, "Error!")` |
| **`status_code`**   | HTTP status of error               | 400, 404, 500                        |
| **Custom handler**  | Centralized error format           | `@app.exception_handler`             |

---

# 🧩 Homework for Day 4

✅ 1. Modify `/divide` so it also accepts a **query parameter** `precision`
👉 Example: `/divide?x=10&y=3&precision=2` → output `3.33`

✅ 2. Add an **extra endpoint `/multiply`** using `async` and proper error handling.
✅ 3. Simulate a slow operation using `await asyncio.sleep(2)` for testing concurrency.

---

# 💬 Real-World Analogy

Think of your FastAPI like a **restaurant** 🍽️

* Each **client request** = a new order
* **async** = multiple chefs working at once
* **await** = waiting for oven to finish, but other chefs still cook
* **HTTPException** = “Sorry, we ran out of ingredients” message instead of kitchen fire 😅

---
