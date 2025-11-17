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

Below are **beautiful, beginner-friendly notes** with **student examples**, **clear explanations**, and **annotated code** — perfect for your learning style and for teaching BSCS students.
I’ve rewritten everything into a **clean, readable, structured** format.

---

# 📘 **FastAPI — Nested Models & Complex Request Bodies**


---

# 🟦 **1. List Fields in Pydantic Models**

## ✅ **A Model Can Have List Attributes**

Example: `tags` is a list.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []   # list of ANY type (not recommended)

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

### ❗ Problem

The list has **no type**, so anything can go inside.

---

---

# 🟦 **2. List With Type Parameter (Better Version)**

## 📌 Python 3.10+ — Type Inside Square Brackets

```python
class Item(BaseModel):
    ...
    tags: list[str] = []  # list of strings only
```

This ensures:

✔ Validation
✔ Auto-docs
✔ Type hints in editors
✔ Clean JSON Schema

---

# 🧑‍🎓 **Student Example — Subjects List**

```python
class Student(BaseModel):
    name: str
    age: int
    subjects: list[str] = []  # only strings allowed
```

### Example JSON sent to API:

```json
{
  "name": "Ali",
  "age": 18,
  "subjects": ["Math", "Physics"]
}
```

---

---

# 🟦 **3. Using Sets Instead of Lists**

Sets store **unique items**, so duplicates are removed automatically.

```python
class Item(BaseModel):
    ...
    tags: set[str] = set()
```

### Student Example — Unique Skills

```python
class Student(BaseModel):
    name: str
    skills: set[str] = set()
```

If input is:

```json
{
  "name": "Sara",
  "skills": ["python", "python", "ml"]
}
```

Output becomes:

```json
{
  "name": "Sara",
  "skills": ["python", "ml"]
}
```

---

---

# 🟦 **4. Nested Models — Models Inside Models**

## 💡 We can use a Pydantic model as a field inside another Pydantic model.

### Example: Student has an Address

```python
class Address(BaseModel):
    city: str
    zipcode: str

class Student(BaseModel):
    name: str
    age: int
    address: Address | None = None
```

### JSON Body Example:

```json
{
  "name": "Hamza",
  "age": 20,
  "address": {
    "city": "Lahore",
    "zipcode": "54000"
  }
}
```

---

---

# 🟦 **5. Using HttpUrl for URL Validation**

FastAPI can validate URLs automatically using `HttpUrl`.

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str
```

If a student uploads an invalid URL → FastAPI rejects it automatically.

---

---

# 🟦 **6. Nested Lists of Models (List[Model])**

Let’s say an item has multiple images.

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    images: list[Image] | None = None
```

### Student Example — A Student with Multiple Test Results

```python
class TestResult(BaseModel):
    subject: str
    marks: int

class Student(BaseModel):
    name: str
    tests: list[TestResult]
```

### JSON Example

```json
{
  "name": "Ali",
  "tests": [
    {"subject": "Math", "marks": 95},
    {"subject": "Physics", "marks": 88}
  ]
}
```

---

---

# 🟦 **7. Deeply Nested Models (Models inside Models inside Models)**

### Example: Offer → contains Items → contains Images

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    price: float
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    price: float
    items: list[Item]
```

---

---

# 🟦 **8. Accepting BODY as a Pure List**

Sometimes API directly accepts a list:

```python
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
```

---

---

# 🟦 **9. Body as Arbitrary Dictionary**

If keys & values are dynamic:

```python
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
```

### Note

JSON keys are always strings → Pydantic converts `"1"` → `1` automatically.

---

---

# 🟩 **📌 BIG RECAP (Exam & Interview Ready)**

### ✔ FastAPI + Pydantic allows:

* List fields (`list[str]`)
* Set fields (`set[str]`)
* Nested models (Model inside model)
* Lists of models (`list[Image]`)
* Deeply nested models (Offer → Item → Image)
* Special types (`HttpUrl`)
* Arbitrary dictionaries (`dict[int, float]`)
* Automatic:

  * Data validation
  * Conversion
  * Documentation (OpenAPI/Swagger)
  * Editor auto-complete

🎯 **All this makes FastAPI one of the fastest + safest API frameworks.**

---
