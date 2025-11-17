Here’s a structured, professional, and internship-ready set of notes on **FastAPI concurrency and async/await** — organized for clarity, with explained syntax, comparison tables, and practical code examples.

***

# FastAPI Roadmap – Day 5: Concurrency and Async / Await

FastAPI provides **asynchronous support** through Python's `async` and `await` syntax. This enables applications to handle many operations efficiently, especially when waiting for external resources (e.g., databases, APIs, file reads).

***

## 1. Synchronous vs Asynchronous Code

| Type | Definition | Example Use Case | Performance |
|------|-------------|-----------------|--------------|
| **Synchronous (`def`)** | Executes one instruction at a time, blocking further tasks until current finishes. | Simple math, CPU-heavy computations. | Slower for I/O-bound tasks. |
| **Asynchronous (`async def`)** | Allows other tasks to run while waiting for I/O operations. | Database queries, API calls, reading files. | Much faster for I/O-bound tasks. |

### Example: Basic comparison

```python
# Synchronous version
@app.get("/sync")
def get_data():
    data = slow_database_query()  # blocking call
    return {"result": data}

# Asynchronous version
@app.get("/async")
async def get_data_async():
    data = await async_database_query()  # non-blocking
    return {"result": data}
```

**Rule:**  
Use `async def` when calling functions that require `await`. Otherwise, use regular `def`.

***

## 2. Understanding async and await

- `async def` defines an asynchronous function (called a **coroutine**).
- `await` suspends function execution until the awaited coroutine/task completes.

### Syntax Example

```python
async def fetch_data():
    await asyncio.sleep(2)  # simulates async I/O wait
    return {"message": "Data fetched"}

@app.get("/data")
async def read_data():
    result = await fetch_data()
    return result
```

`await` can only be used **inside** `async def` functions.  

***

## 3. When to Use `async` and `await`

| Situation | Path Function Type | Example |
|------------|-------------------|----------|
| You call an async-compatible library (`await` required) | `async def` | `results = await async_lib()` |
| You use a blocking library (no async support) | `def` | `results = blocking_lib()` |
| You're unsure which to use | `def` | Safer default |

### Example

```python
# Async library support
@app.get("/items")
async def get_items():
    data = await async_api_call()
    return data

# Blocking I/O library
@app.get("/users")
def get_users():
    users = legacy_db.get_all()  # blocking call
    return users
```

FastAPI internally handles both efficiently using thread pools when necessary.

***

## 4. Concurrency vs Parallelism

| Concept | Description | Analogy | Best For |
|----------|--------------|----------|-----------|
| **Concurrency** | Tasks appear to run simultaneously by switching between them. | Taking multiple burger orders while waiting for them to cook. | I/O-bound tasks |
| **Parallelism** | Tasks actually run at the same time on multiple CPUs. | Several chefs cooking burgers at once. | CPU-bound tasks |

- Concurrency ≠ Parallelism  
- Concurrency handles **many I/O tasks efficiently**.  
- Parallelism uses **multiple processors for heavy computation**.

***

## 5. I/O Bound vs CPU Bound

| Type | Description | Example Tasks | Handling Method |
|------|--------------|---------------|----------------|
| I/O Bound | Waiting for external data sources (network, disk). | API calls, database queries. | Use async/await (FastAPI built-in). |
| CPU Bound | Processor-intensive work. | ML model inference, image processing. | Use multiprocessing / background tasks. |

***

## 6. Mixing def and async def

FastAPI allows both styles in the same app.

```python
@app.get("/async_task")
async def async_task():
    return {"async_result": await some_async_func()}

@app.get("/sync_task")
def sync_task():
    return {"sync_result": some_blocking_func()}
```

FastAPI automatically:
- Runs sync functions in a **thread pool**.
- Awaits async functions directly.

***

## 7. Writing your own async code

Using `asyncio` or `AnyIO`, you can write custom asynchronous functions.

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

async def simulate_network_call():
    await asyncio.sleep(2)
    return "Network data"

@app.get("/network")
async def get_network_data():
    data = await simulate_network_call()
    return {"response": data}
```

If deeper control is needed, explore **AnyIO** or **Asyncer** for structured concurrency.

***

## 8. Combining Asynchronous + Parallel Processing

In AI / ML backends:
- Use **async FastAPI routes** to handle concurrent web requests.
- Use **parallel processes** (like `multiprocessing`, Celery, or GPU tasks) for model inference.

Example:

```python
from fastapi import FastAPI
import asyncio
import concurrent.futures

app = FastAPI()

def cpu_heavy_task(n):
    return sum(i * i for i in range(n))

@app.get("/train")
async def train_model():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_heavy_task, 10_000_000)
    return {"result": result}
```

This design lets the API handle many training requests concurrently while running heavy work in parallel processes.

***

## 9. FastAPI and Async Under the Hood

- FastAPI uses **Starlette**, which is built on **AnyIO**, compatible with **asyncio** and **Trio**.  
- Blocking route (`def`) → runs in **thread pool**.  
- Async route (`async def`) → event loop schedules it directly.  
- FastAPI auto-optimizes both cases for best performance.

***

## 10. Key Takeaways

1. Use `async def` for I/O-bound operations.
2. Use `def` for blocking or CPU-bound libraries.
3. You can mix both freely — FastAPI manages them effectively.
4. Parallelism (for ML compute) can be added using multiprocessing or GPU threads.
5. FastAPI ≈ NodeJS-level async performance + Python’s ML ecosystem.

***

### Practice Exercise

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

async def fetch_user(id):
    await asyncio.sleep(1)
    return {"id": id, "name": f"User{id}"}

@app.get("/users/all")
async def get_all_users():
    results = await asyncio.gather(fetch_user(1), fetch_user(2), fetch_user(3))
    return results
```
Runs all `fetch_user` calls **concurrently** — total time ≈ 1s instead of 3s.

***

Would you like a **follow-up visual cheat sheet (diagram + async vs sync flow)** to help solidify this section for your AI engineer portfolio notebook?