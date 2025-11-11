## FastAPI `Path()` Function Details

The `Path()` function in FastAPI is used to provide metadata, validation rules, and documentation hints for path parameters in your API endpoints.

### Features

- **Title**
- **Description**
- **Example**
- **ge**, **gt**, **le**, **lt**
- **Min_length**
- **Max_length**
- **regex**


```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., title="The ID of the item to get")):
return {"item_id": item_id}

```


Here’s your **entire README** in **one single Markdown cell** so you can just copy-paste without breaking anything:

```markdown
# 🏥 Patient API with FastAPI

This project is a simple **FastAPI** application that loads patient data from a `patients.json` file and provides endpoints to retrieve **all patient records** or **details for a specific patient**.

---

## 📂 Project Structure
```

.
├── main.py             # FastAPI application code
├── patients.json       # Patient data in JSON format
└── README.md           # Documentation file

````

---

## ⚙️ Requirements
- **Python 3.8+**
- Install dependencies:
```bash
pip install fastapi uvicorn
````

---

## 📜 Code Explanation

```python
from fastapi import FastAPI, Path
import json
```

* **FastAPI** → Used to create the API.
* **Path** → Used to declare and document path parameters.
* **json** → Loads data from `patients.json`.

```python
app = FastAPI()
```

* Creates an **instance** of the FastAPI application.

```python
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data
```

* **load\_data()** → Helper function to open `patients.json` and return its contents as a Python dictionary.

---

### **Root Endpoint**

```python
@app.get("/")
async def root():
    return {'Info': 'This is the best platform to get doctors details of all over the world.'}
```

* **Method**: `GET`
* **Path**: `/`
* **Description**: Returns a welcome/info message.

---

### **View All Patients**

```python
@app.get('/view')
def view():
    data = load_data()
    return data
```

* **Method**: `GET`
* **Path**: `/view`
* **Description**: Returns **all patient records** from `patients.json`.

---

### **View Specific Patient**

```python
@app.get('/view/{patient_id}')
def view_patient(
    patient_id: str = Path(
        ..., 
        description='The ID of the patient to get details of', 
        title='Patient ID', 
        example='P001'
    )
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        return {'Error': 'Patient not found'}
```

* **Method**: `GET`
* **Path**: `/view/{patient_id}`
* **Description**: Fetch details of a specific patient using their `patient_id`.
* **Path Parameter**:

  * `patient_id` → String, required.
  * **Example**: `"P001"`

---

## 🗂 Example `patients.json` File

```json
{
    "P001": {
        "name": "John Doe",
        "age": 34,
        "disease": "Flu",
        "doctor": "Dr. Smith"
    },
    "P002": {
        "name": "Jane Roe",
        "age": 29,
        "disease": "Diabetes",
        "doctor": "Dr. Brown"
    }
}
```

---

## 🚀 Running the Application

Run with **Uvicorn**:

```bash
uvicorn main:app --reload
```

* **`main`** → Python file name (without `.py`)
* **`app`** → FastAPI instance variable
* **`--reload`** → Auto-reloads when you make changes.

---

## 📌 API Endpoints

| Method | Endpoint             | Description        | Example URL                       |
| ------ | -------------------- | ------------------ | --------------------------------- |
| GET    | `/`                  | Welcome message    | `http://127.0.0.1:8000/`          |
| GET    | `/view`              | View all patients  | `http://127.0.0.1:8000/view`      |
| GET    | `/view/{patient_id}` | View patient by ID | `http://127.0.0.1:8000/view/P001` |

---

## 🌐 API Testing with cURL

**1. Root Endpoint**

```bash
curl http://127.0.0.1:8000/
```

**2. All Patients**

```bash
curl http://127.0.0.1:8000/view
```

**3. Specific Patient**

```bash
curl http://127.0.0.1:8000/view/P001
```

---

## 📄 API Documentation (Swagger UI)

FastAPI automatically generates Swagger UI and ReDoc:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠 Error Handling Example

If a patient ID is not found:

```json
{
    "Error": "Patient not found"
}
```

---

## 💡 Notes

* Ensure `patients.json` exists in the same directory as `main.py`.
* Update `patients.json` to add or modify patient data.

---

## 📜 License

This project is open-source and available under the **MIT License**.

```

---

I can also give you a **visually attractive API architecture diagram** in the same Markdown so your README looks professional on GitHub. Do you want me to add that?
```
