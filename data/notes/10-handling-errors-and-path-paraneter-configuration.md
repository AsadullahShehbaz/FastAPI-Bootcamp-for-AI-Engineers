

# 📘 **FastAPI Error Handling – Easy Notes (School Examples)**

When building an API, things can go wrong:

* A student ID might not exist
* A teacher may not have permission
* A book might be missing
* User sends wrong data type (e.g., “age”: “twelve”)

FastAPI gives clear ways to **raise errors**, **customize errors**, and **handle them globally**.

---

# ⭐ 1. **Use HTTPException**

FastAPI gives a built-in exception called **HTTPException** to send proper error messages.

### ➤ Example: Student Not Found

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

students = {"ali": "Grade 8", "sara": "Grade 7"}

@app.get("/students/{student_name}")
async def get_student(student_name: str):
    if student_name not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": students[student_name]}
```

### ✔ Output if student exists

```json
{ "student": "Grade 8" }
```

### ❌ Output if student not found

```json
{ "detail": "Student not found" }
```

---

# ⭐ 2. **HTTPException Can Use Any JSON Data**

You can send a **dict**, **list**, etc.

Example:

```python
raise HTTPException(
    status_code=400,
    detail={"error": "Invalid class number", "hint": "Use class 1–10"}
)
```

---

# ⭐ 3. **Add Custom Headers to Error**

Useful for advanced things (security, logging, rate-limit messages).

### ➤ Example: Adding a custom error header

```python
@app.get("/students-header/{name}")
async def get_student_header(name: str):
    if name not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
            headers={"X-Error": "StudentMissing"}
        )
    return {"student": students[name]}
```

---

# ⭐ 4. **Create Custom Exceptions (Your Own Error Classes)**

Imagine the school has a special rule:

* Student **“joker”** is banned temporarily.

### ➤ Step 1: Make a custom exception

```python
class BannedStudentException(Exception):
    def __init__(self, name: str):
        self.name = name
```

### ➤ Step 2: Create an exception handler

```python
from fastapi.responses import JSONResponse

@app.exception_handler(BannedStudentException)
async def banned_student_handler(request, exc: BannedStudentException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Student {exc.name} is banned from school."},
    )
```

### ➤ Step 3: Use it in a route

```python
@app.get("/check/{name}")
async def check_student(name: str):
    if name == "joker":
        raise BannedStudentException(name)
    return {"status": "Allowed"}
```

---

# ⭐ 5. **Override Default FastAPI Error Handlers**

FastAPI already handles:

* `HTTPException`
* `RequestValidationError` (wrong data type)

You can replace these with your own.

---

## 🟦 A. Override Request Data Validation Errors (Wrong inputs)

Example: Student roll number must be **integer**, but user sends text.

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
```

### ➤ Student API

```python
@app.get("/roll/{roll_no}")
async def get_roll(roll_no: int):
    return {"roll_no": roll_no}
```

### ❌ If user requests:

```
/roll/abc
```

👉 Response will be plain text:

```
1 validation error
path -> roll_no
  value is not a valid integer (type=type_error.integer)
```

---

## 🟦 B. Override HTTPException Handler (Custom style)

```python
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
```

---

# ⭐ 6. **Use the Request Body Inside Validation Error**

Very useful for debugging when user sends wrong data.

### ➤ Example: School Item Model

```python
from pydantic import BaseModel

class SchoolItem(BaseModel):
    title: str
    quantity: int
```

### ➤ Custom exception handler

```python
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def body_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": exc.body
        })
    )
```

### ❌ Wrong request body

```json
{
  "title": "Markers",
  "quantity": "Ten"
}
```

### 👉 Output shows exact error + full wrong body

```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "Markers",
    "quantity": "Ten"
  }
}
```

---

# ⭐ 7. **Reuse FastAPI Default Exception Handlers**

Sometimes you want to:

* Log errors
* Print messages
* Then still use default FastAPI handler

### ➤ Example

```python
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_handler(request, exc):
    print("HTTP Error:", exc)
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def custom_validation_handler(request, exc):
    print("Validation Error:", exc)
    return await request_validation_exception_handler(request, exc)
```

---

# 🎯 **Final Summary**

| Concept                  | Why We Use It                                 |
| ------------------------ | --------------------------------------------- |
| `HTTPException`          | Return normal API errors (404, 400, etc.)     |
| Custom headers           | Advanced metadata (e.g., rate-limit messages) |
| Custom exceptions        | Define your own error types                   |
| Override handlers        | Change how FastAPI sends errors               |
| `RequestValidationError` | Handle incorrect input data                   |
| Reuse handlers           | Keep default behavior + add logging           |

---

# 🎒 **School Theme Quick Example**

```python
@app.get("/class/{class_id}")
async def get_class(class_id: int):
    if class_id not in [1,2,3,4,5,6,7,8,9,10]:
        raise HTTPException(
            status_code=400,
            detail={"error": "Class does not exist", "allowed": "1 to 10"}
        )
    return {"class": class_id}
```


# 🌟 **FastAPI — Path Operation Configuration (Smart Notes)**

*Master how to enhance, organize, and document your API endpoints using clean metadata.*

FastAPI allows you to **configure each path operation** (endpoint) using powerful decorator parameters.
These parameters define how your API behaves, appears in documentation, and communicates with clients.

> ⚠️ **Important:**
> These parameters are added **to the decorator**, NOT inside the function.

---

# 1️⃣ **Response Status Code**

Every endpoint returns an HTTP status code.
You can set it using the `status_code` parameter.

### ✔ Two Ways to Set Status Code

### **1. Direct integer**

```python
@app.post("/items/", status_code=201)
```

### **2. Using FastAPI’s readable constants (Recommended)**

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
```

✨ **Benefit:** More readable, less error-prone.
✨ This status is automatically included in the **OpenAPI docs**.

### Example:

```python
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

---

# 2️⃣ **Tags – Organize Your API**

Tags help group similar endpoints in Swagger UI.

### Example:

```python
@app.post("/items/", tags=["items"])
async def create_item(item: Item):
    return item
```

Swagger UI will group:

* `/items/` under **items**
* `/users/` under **users**

### Benefits:

* Clean documentation
* Easy navigation
* Perfect for large projects

---

# 3️⃣ **Tags Using Enums (Clean Architecture)**

For big apps, tags can get messy.
Use an **Enum** to centralize tag definitions.

### Example:

```python
from enum import Enum

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
def read_items():
    return [...]
```

✨ Keeps tag names consistent across your project.
✨ Eliminates typos.

---

# 4️⃣ **Add Summary and Description**

Helps document your API professionally.

### Example:

```python
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with name, description, price, tax and tags."
)
async def create_item(item: Item):
    return item
```

### Where does it show?

* Swagger UI
* Redoc UI
* OpenAPI schema

---

# 5️⃣ **Using Docstring as Description (Smart Technique)**

Instead of writing long descriptions in the decorator,
you can write them inside the function docstring.

FastAPI automatically picks it up!

### Example:

```python
@app.post("/items/", summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all details:

    - **name**: required
    - **description**: optional
    - **price**: required
    - **tax**: optional
    - **tags**: set of unique strings
    """
    return item
```

### Benefits:

✔ Cleaner decorator
✔ Multi-line Markdown
✔ Professional documentation

---

# 6️⃣ **Response Description**

Defines what the **response itself** represents.

```python
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    return item
```

Difference:

* `description` → describes the *endpoint*
* `response_description` → describes the *output*

If you don’t provide one, FastAPI auto-fills:
👉 `"Successful response"`

---

# 7️⃣ **Deprecating a Path Operation**

When an endpoint is outdated but must remain functional, mark it as **deprecated**.

```python
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
```

In Swagger UI:
⚠️ It will appear with a **deprecated warning** and crossed styling.

### Why deprecate?

* Migrating to new endpoints
* Versioning
* Gradual API updates

---

# 🧠 **Recap — What Can You Configure?**

| Feature                | Purpose                        |
| ---------------------- | ------------------------------ |
| `status_code`          | Set correct HTTP response code |
| `tags`                 | Group operations in docs       |
| `summary`              | Short endpoint explanation     |
| `description`          | Full Markdown description      |
| Docstring description  | Cleaner multi-line docs        |
| `response_description` | Explain the output             |
| `deprecated=True`      | Mark an endpoint as outdated   |

---

# 🎁 **Bonus: Cleanest Possible Endpoint Example**

```python
@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create an item",
    description="Add a new item with full details like name, price, tax, and tags.",
    response_description="The newly created item",
)
async def create_item(item: Item):
    """
    ### Details Required:
    - **name**: Name of the item
    - **description**: Optional long text
    - **price**: Must be a float
    - **tax**: Optional float
    - **tags**: Unique set of strings

    Returns the complete item model after creation.
    """
    return item
```
