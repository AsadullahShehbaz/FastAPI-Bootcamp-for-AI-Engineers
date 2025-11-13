

---

# Pagination, Input Validation, Error Handling, and Logging — Step-by-Step Notes

---

## 1. **Pagination**

### What is pagination?

* It divides the data into smaller chunks (pages) to limit the number of records returned in a single response.
* Common parameters: `skip` (offset), `limit` (number of records per page).

### How to add pagination in FastAPI:

* Use query parameters to receive `skip` and `limit` from the client.
* Pass them to your database query to control the subset of data returned.

### Example:

```python
from typing import List
from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

fake_db = [{"id": i, "name": f"item_{i}"} for i in range(1, 101)]  # Sample data 1 to 100

@app.get("/items/", response_model=List[dict])
def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip: skip + limit]
```

### Notes:

* Set default values (e.g., `skip=0`, `limit=10`).
* You can enforce max limits for `limit` (e.g., max 50).
* Use FastAPI’s `Query` for extra validation (min/max).

---

## 2. **Input Validation**

### What is input validation?

* Ensures incoming data (path, query, body) matches expected format & constraints.
* Prevents bad data and improves API reliability.

### FastAPI validation tools:

* Pydantic models for JSON body validation.
* Built-in validation for query/path parameters (e.g., types, constraints).
* Use `Query()`, `Path()`, and `Body()` for additional constraints.

### Example with Query validation:

```python
from fastapi import Query

@app.get("/search/")
def search_items(q: str = Query(..., min_length=3, max_length=50)):
    return {"query": q}
```

### Notes:

* `...` means required parameter.
* Use constraints like `min_length`, `max_length`, `gt` (greater than), `le` (less or equal).
* Validate request body using Pydantic models with field types and validators.

---

## 3. **Improved Error Responses**

### What is improved error handling?

* Return clear, consistent, and meaningful error messages and HTTP status codes.
* Helps clients debug issues easier.

### How to do it in FastAPI:

* Use `HTTPException` to return HTTP errors.
* Customize error details.
* Use exception handlers for common errors.

### Example:

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 1 or item_id > 100:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

### Advanced:

* Create custom exception handlers with `@app.exception_handler()`.
* Validate user input and return `400 Bad Request` if invalid.
* Return `422 Unprocessable Entity` automatically on Pydantic validation errors.

---

## 4. **Basic Logging**

### Why logging?

* Track API requests, errors, and flow for debugging and monitoring.
* Helps in production troubleshooting.

### How to add logging in FastAPI:

* Use Python’s built-in `logging` module.
* Add middleware to log incoming requests and responses.

# Step-by-step explanation — teaching style (for a new student)

Nice — this is a compact, practical logging configuration using Python’s `logging.config.dictConfig`. I’ll walk you through **every line and concept**, show how to **turn it on**, demonstrate **how to use it**, and give **best-practice tips** you can apply immediately.

---

## 1) What this snippet does at a high level

The code defines a **logging configuration dictionary** (`LOGGING_CONFIG`) that:

* formats log messages,
* sends logs both to a **file** and to the **console**,
* sets the root logger level to `DEBUG` (so everything `DEBUG` and above is captured),
* and is intended to be applied with `dictConfig(LOGGING_CONFIG)` so your app starts logging accordingly.

It’s a programmatic replacement for a `logging.conf` file.

---

## 2) The code (annotated)

```python
import logging
from logging.config import dictConfig

# Simple logging config 
LOGGING_CONFIG = {
    'version':1,                     # 1 = required by dictConfig schema
    'formatters':{                   # how messages are formatted
        'default':{
            'format':'[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers':{                     # where logs go (file, console, etc.)
        'file':{
            'class':'logging.FileHandler',
            'filename':'logs/school_api.log',
            'formatter':'default',
        },
        'console':{
            'class':'logging.StreamHandler',
            'formatter':'default',
        }, 
    },
    'loggers':{                      # logger definitions ('' = root logger)
        '':{
            'level':'DEBUG',
            'handlers':['file','console'],
        },
    }
}
```

Now step-by-step.

---

## 3) `version: 1`

* **What:** Required by the `logging.config.dictConfig` spec. Always set `'version': 1`.
* **Why:** The config system might evolve; the version field identifies the schema.

---

## 4) `formatters` — shaping the message text

Formatter named `"default"` with format:

```
[%(asctime)s] %(levelname)s in %(module)s: %(message)s
```

* `%(asctime)s` — timestamp (human readable).
* `%(levelname)s` — log severity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
* `%(module)s` — the Python module name where the log call came from.
* `%(message)s` — the message you pass to `logger.info(...)`.

**Resulting example:**

```
[2025-11-14 23:12:01,123] INFO in main: Server started
```

---

## 5) `handlers` — where the messages go

Two handlers:

* **`file`** handler uses `logging.FileHandler`

  * Writes logs to the file `logs/school_api.log`.
  * Uses the `'default'` formatter.
* **`console`** handler uses `logging.StreamHandler`

  * Writes to the standard stream (usually terminal).
  * Also uses `'default'` formatter.

Handlers are modular: you can add others (SMTP, HTTP, rotating file, etc.).

**Important note:** `FileHandler` will try to open `logs/school_api.log`. If `logs/` directory does not exist, you’ll get an error. Create the folder first:

```bash
mkdir -p logs
```

---

## 6) `loggers` — which loggers use which handlers

You defined an entry with the key `''` (empty string) — that means **the root logger**.
Root logger settings apply to all loggers by default unless a child logger overrides them.

* `'level': 'DEBUG'` — capture messages from DEBUG and above.
* `'handlers': ['file', 'console']` — the root logger will emit every message to both handlers.

Why use root logger? For small apps it’s simple; for larger apps, define named loggers per module.

---

## 7) How to activate it in your app

Call `dictConfig(LOGGING_CONFIG)` once at startup (before other modules log):

```python
from logging.config import dictConfig
from your_logging_module import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)
import logging

logger = logging.getLogger(__name__)
logger.info("Logging configured. Hello world.")
```

`__name__` logger will inherit root config and send logs to both file and console.

---

## 8) How to use logging in modules (example)

In `main.py`:

```python
import logging

logger = logging.getLogger(__name__)

def start_app():
    logger.debug("Debugging start_app")
    logger.info("Starting app")
    try:
        1 / 0
    except Exception:
        logger.exception("Something broke")  # logs stack trace at ERROR
```

`logger.exception()` logs the stack trace automatically — use it in `except` blocks.

---

## 9) Example output (console + file)

Console and file will show same formatted messages:

```
[2025-11-14 23:12:01,123] DEBUG in main: Debugging start_app
[2025-11-14 23:12:01,124] INFO in main: Starting app
[2025-11-14 23:12:01,125] ERROR in main: Something broke
Traceback (most recent call last):
  File "main.py", line 12, in start_app
    1/0
ZeroDivisionError: division by zero
```

---

## 10) Practical best-practices & improvements

1. **Create `logs/` beforehand**

   ```python
   import os
   os.makedirs("logs", exist_ok=True)
   ```

2. **Prefer named loggers in large apps**

   * Use `logger = logging.getLogger(__name__)` in every module.
   * Configure per-module levels if needed:

     ```python
     'loggers': {
         'uvicorn': {'level': 'INFO', 'handlers': ['console']},
         'myapp.db': {'level': 'WARNING', 'handlers': ['file']}
     }
     ```

3. **Use rotating file handlers to avoid huge files**
   Replace `'class': 'logging.FileHandler'` with:

   * `'logging.handlers.RotatingFileHandler'` — rotate by size.
   * `'logging.handlers.TimedRotatingFileHandler'` — rotate by time.

   Example (dictConfig):

   ```py
   'file': {
       'class': 'logging.handlers.RotatingFileHandler',
       'filename': 'logs/school_api.log',
       'maxBytes': 10_000_000,
       'backupCount': 5,
       'formatter': 'default'
   }
   ```

4. **Use environment variables for log level**

   * Toggle `DEBUG`/`INFO` by env var in production.
   * Avoid verbose `DEBUG` in production.

5. **Avoid logging secrets**

   * Never log passwords, tokens, or PII.

6. **Structured logging**

   * For JSON logs (useful in production), use a JSON formatter (third-party packages like `python-json-logger`).

---

## 11) Troubleshooting common issues

* **FileNotFoundError**: create `logs/` folder.
* **No logs appearing**: ensure `dictConfig(LOGGING_CONFIG)` runs before modules do any logging.
* **Duplicate logs**: caused by handlers added twice or `propagate=True`. If you configure child loggers and want to avoid double output, set `propagate: False` on that child logger.

---

## 12) Minimal runnable example (put everything together)

```python
# run_logger_example.py
import os
from logging.config import dictConfig
import logging

LOGGING_CONFIG = {
    'version':1,
    'formatters':{
        'default':{
            'format':'[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers':{
        'file':{
            'class':'logging.FileHandler',
            'filename':'logs/school_api.log',
            'formatter':'default',
        },
        'console':{
            'class':'logging.StreamHandler',
            'formatter':'default',
        },
    },
    'loggers':{
        '':{
            'level':'DEBUG',
            'handlers':['file','console'],
        },
    }
}

os.makedirs("logs", exist_ok=True)
dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.info("Logger initialized")
logger.debug("This is a debug message")
try:
    1/0
except Exception:
    logger.exception("We caught an exception")
```

Run it and check `logs/school_api.log`.

---

## 13) Quick checklist for the student

* [ ] Call `dictConfig()` early in startup.
* [ ] Create `logs/` directory before using `FileHandler`.
* [ ] Use `logger = logging.getLogger(__name__)` in every module.
* [ ] Don’t log secrets or PII.
* [ ] Swap `FileHandler` for rotating handlers in production.
* [ ] Use environment variables to control log levels.

---


### Notes:

* Configure log format, level (`DEBUG`, `INFO`, `WARNING`, etc.).
* Log important events and errors inside your endpoint functions.
* You can integrate with advanced loggers like `loguru` or external systems later.

---

# Summary

| Feature                  | What to Do                            | FastAPI Tool / Method                          |
| ------------------------ | ------------------------------------- | ---------------------------------------------- |
| Pagination               | Limit/offset queries                  | Query params `skip`, `limit` + slicing         |
| Input Validation         | Validate query/body/path inputs       | Pydantic models + `Query()`, `Path()`          |
| Improved Error Responses | Raise `HTTPException` with clear info | `raise HTTPException(status_code, detail=...)` |
| Basic Logging            | Log requests and responses            | Python `logging` + middleware                  |

---


