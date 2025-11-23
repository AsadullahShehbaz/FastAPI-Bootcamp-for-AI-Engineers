### Day 8-9: File Upload & Processing in FastAPI

Welcome back to our FastAPI learning series! As an AI Engineer, I'll guide you through handling file uploads and processing in FastAPI. This is a crucial feature for building APIs that deal with user-submitted files, such as images for profiles, PDFs for documents, or CSVs for data import.

FastAPI makes file uploads straightforward by leveraging Starlette's `UploadFile` class (which FastAPI builds upon). It supports asynchronous handling, automatic multipart/form-data parsing, and easy integration with Pydantic for validation.

#### Key Concepts

1. **File Uploads (Images, PDFs, CSV)**:
   - Use the `UploadFile` type hint in your endpoint parameters to accept files.
   - Files are uploaded via HTTP POST with `multipart/form-data` encoding.
   - You can access file metadata (e.g., filename, content_type) and content (e.g., via `file.read()` or `file.save()`).
   - Processing examples:
     - Images: Save to disk or process with libraries like Pillow.
     - PDFs: Extract text using libraries like PyPDF2.
     - CSVs: Parse with `csv` module or pandas.

2. **Form Data Handling**:
   - Use `Form(...)` for non-file form fields (e.g., strings, integers).
   - Combine with `UploadFile` for mixed form + file submissions.
   - FastAPI automatically handles form parsing.

3. **Multipart Requests**:
   - These are HTTP requests that send multiple parts (e.g., form fields + files) in one payload.
   - FastAPI/Starlette handles this out-of-the-box when you define parameters with `Form` and `UploadFile`.
   - No need for manual parsing—it's all declarative.

4. **File Validation**:
   - Validate file type (e.g., check `content_type` or file extension).
   - Validate size (e.g., limit to 10MB).
   - Validate content (e.g., ensure CSV has required headers).
   - Use dependencies or custom logic in the endpoint for validation.
   - Raise `HTTPException` for invalid files.

#### Prerequisites
- Install FastAPI and Uvicorn: `pip install fastapi uvicorn`
- For processing examples:
  - Images: `pip install pillow`
  - PDFs: `pip install pypdf2`
  - CSVs: `pip install pandas` (optional; built-in `csv` works too)
- Run the app: `uvicorn main:app --reload`

#### Full Example Code
Below is a complete, runnable FastAPI application demonstrating all the topics. It includes a single endpoint `/upload/` that accepts a file (image, PDF, or CSV) along with a form field (description). It validates the file, processes it based on type, and returns a response.

Create a file named `main.py`:

```python
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import os
import shutil
from PIL import Image  # For image processing
import PyPDF2  # For PDF processing
import csv  # For CSV processing
import pandas as pd  # Optional for advanced CSV handling

app = FastAPI(title="FastAPI File Upload & Processing Demo")

# Directory to save uploaded files (create it if it doesn't exist)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency for file validation (reusable)
async def validate_file(file: UploadFile = File(...)):
    # Allowed file types
    allowed_types = {
        "image": ["image/jpeg", "image/png"],
        "pdf": ["application/pdf"],
        "csv": ["text/csv"]
    }
    
    # Check content type
    content_type = file.content_type
    file_type = None
    if content_type in allowed_types["image"]:
        file_type = "image"
    elif content_type in allowed_types["pdf"]:
        file_type = "pdf"
    elif content_type in allowed_types["csv"]:
        file_type = "csv"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: images (jpg/png), PDFs, CSVs.")
    
    # Check file size (limit to 10MB)
    await file.seek(0)  # Reset file pointer
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB.")
    
    # Additional type-specific validation
    if file_type == "csv":
        await file.seek(0)  # Reset again for reading
        try:
            reader = csv.reader((await file.read()).decode('utf-8').splitlines())
            headers = next(reader)
            if "name" not in headers or "age" not in headers:  # Example: Require specific headers
                raise ValueError("Missing required headers")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV format.")
    
    await file.seek(0)  # Reset for processing
    return file_type, file

@app.post("/upload/")
async def upload_file(
    description: str = Form(..., description="A description of the uploaded file"),
    file: UploadFile = File(...),
    validated: tuple = Depends(validate_file)
):
    file_type, file = validated  # From dependency
    
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process based on file type
    processing_result = {}
    
    if file_type == "image":
        # Example: Resize image and get dimensions
        with Image.open(file_path) as img:
            img.thumbnail((128, 128))  # Resize
            img.save(file_path)  # Overwrite with resized version
            processing_result = {
                "original_size": img.size,
                "resized": True,
                "format": img.format
            }
    
    elif file_type == "pdf":
        # Example: Extract text from first page
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()
                processing_result = {
                    "page_count": len(reader.pages),
                    "first_page_text": text[:100] + "..."  # Truncate for brevity
                }
            else:
                processing_result = {"error": "Empty PDF"}
    
    elif file_type == "csv":
        # Example: Read CSV and compute stats (using pandas for simplicity)
        df = pd.read_csv(file_path)
        processing_result = {
            "row_count": len(df),
            "columns": list(df.columns),
            "sample_data": df.head(1).to_dict(orient="records")
        }
    
    return JSONResponse(content={
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "description": description,
        "processing_result": processing_result
    })

# Optional: Cleanup endpoint for demo purposes (not production-ready)
@app.delete("/cleanup/")
async def cleanup_uploads():
    for filename in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, filename))
    return {"message": "Uploads directory cleaned"}
```

#### Explanation of the Code

- **Endpoint Setup**: The `/upload/` endpoint uses `POST` and accepts a form field (`description`) and a file (`file`).
- **Form Data Handling**: `description = Form(...)` captures string form data.
- **Multipart Requests**: Handled implicitly by FastAPI when mixing `Form` and `UploadFile`.
- **File Validation**: Done via a dependency `validate_file`. It checks type, size, and CSV-specific content. If invalid, raises `HTTPException` (returns 400 Bad Request).
- **Processing**:
  - **Image**: Uses Pillow to resize and get metadata.
  - **PDF**: Uses PyPDF2 to extract page count and text.
  - **CSV**: Uses pandas to read and summarize data.
- **Saving Files**: Files are saved to an `uploads` directory. In production, use temporary files or cloud storage (e.g., S3) instead.
- **Response**: Returns JSON with details and processing results.

#### Testing the API
1. Run the app: `uvicorn main:app --reload`
2. Use tools like Postman or curl:
   - POST to `http://127.0.0.1:8000/upload/`
   - Add form field: `description` = "My test file"
   - Add file: Upload an image/PDF/CSV
3. Interactive Docs: Visit `http://127.0.0.1:8000/docs` and test via Swagger UI.
4. Example curl for image upload:
   ```
   curl -X POST "http://127.0.0.1:8000/upload/" \
   -F "description=My image" \
   -F "file=@/path/to/image.jpg"
   ```

#### Best Practices & Tips
- **Security**: Always validate files to prevent malicious uploads (e.g., executables disguised as images). Use antivirus scanning in production.
- **Async Handling**: `UploadFile` supports async reads for large files.
- **Streaming**: For huge files, stream directly without saving to disk (e.g., `await file.read()`).
- **Error Handling**: Catch exceptions in processing to avoid 500 errors.
- **Limits**: Configure Uvicorn/FastAPI for max request size if needed.
- **Extensions**: Integrate with background tasks (e.g., via `BackgroundTasks`) for long-processing files.

Practice by modifying the code—add more validations or process multiple files (`List[UploadFile]`). If you have questions or want Day 10 notes, let me know!