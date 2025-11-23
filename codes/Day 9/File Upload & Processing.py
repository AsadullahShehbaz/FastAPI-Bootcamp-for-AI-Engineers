"""
FastAPI File Upload & Processing Demo 📸📄📊
A clean, educational example showing how to:
- Accept file uploads (images, PDFs, CSVs)
- Validate file type & size safely
- Process each file type differently
- Return meaningful results
Perfect for beginners learning FastAPI + file handling!
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Tuple
import os
import shutil
from PIL import Image
import PyPDF2
import csv
import pandas as pd

# ------------------------------------------------------------------
# App Initialization – Give your API a nice name and description!
# ------------------------------------------------------------------
app = FastAPI(
    title="FastAPI File Upload & Processing Demo",
    description="Upload images, PDFs, or CSVs and see smart processing in action! 🚀",
    version="1.0.0"
)

# ------------------------------------------------------------------
# Configuration – Where do we store uploaded files?
# ------------------------------------------------------------------
UPLOAD_DIR = "uploads"                     # Folder to save uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True)     # Create it if it doesn't exist yet


# ------------------------------------------------------------------
# Dependency: File Validation – The guardian of our endpoint! 🛡️
# Validates file type, size, and even CSV structure before processing.
# ------------------------------------------------------------------
async def validate_file(file: UploadFile = File(...)) -> Tuple[str, UploadFile]:
    """
    Ensures only safe and expected files get through.
    Returns a tuple: (file_type, original_file_with_cursor_reset)
    """
    # Allowed MIME types – easy to extend later!
    allowed_types = {
        "images": ["image/jpeg", "image/png"],
        "pdfs":   ["application/pdf"],
        "csvs":   ["text/csv"]
    }

    content_type = file.content_type
    file_type = None

    # Detect file category based on MIME type
    if content_type in allowed_types["images"]:
        file_type = "image"
    elif content_type in allowed_types["pdfs"]:
        file_type = "pdf"
    elif content_type in allowed_types["csvs"]:
        file_type = "csv"
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type 😔 Only JPEG/PNG images, PDFs, and CSVs are allowed."
        )

    # Read file content once for size check (we'll reset cursor later)
    await file.seek(0)
    content = await file.read()

    # Safety first: limit file size to 10 MB
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large! 📏 Maximum allowed size is 10MB."
        )

    # Extra validation for CSV files – must have 'name' and 'age' columns
    if file_type == "csv":
        await file.seek(0)
        try:
            # Decode and peek at the first row (headers)
            text_content = (await file.read()).decode("utf-8")
            reader = csv.reader(text_content.splitlines())
            headers = next(reader)

            if "name" not in headers or "age" not in headers:
                raise ValueError("CSV must contain 'name' and 'age' columns")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Invalid CSV format ❌ – Make sure it has 'name' and 'age' headers."
            )

    # Reset cursor so the file can be read again when saving/processing
    await file.seek(0)
    return file_type, file


# ------------------------------------------------------------------
# Main Endpoint: /upload/ – The star of the show! 🌟
# Handles file upload + description + smart processing based on type
# ------------------------------------------------------------------
@app.post("/upload/")
async def upload_file(
    description: str = Form(..., description="A short description of what this file is about"),
    file: UploadFile = File(...),
    validated: Tuple[str, UploadFile] = Depends(validate_file)
):
    """
    Upload a file, get it processed magically, and receive a friendly JSON response!
    """
    file_type, file_obj = validated  # Unpack our validated data

    # Save the uploaded file to disk
    file_path = os.path.join(UPLOAD_DIR, file_obj.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_obj.file, buffer)

    # Dictionary to store processing results – different for each file type
    processing_result = {}

    # ------------------------------------------------------------------
    # Image Processing – Resize to thumbnail (128x128) 📸
    # ------------------------------------------------------------------
    if file_type == "image":
        with Image.open(file_path) as img:
            original_size = img.size
            img.thumbnail((128, 128))         # Keeps aspect ratio!
            img.save(file_path)               # Overwrite with smaller version
            processing_result = {
                "original_size": original_size,
                "new_size": img.size,
                "resized": True,
                "format": img.format,
                "message": "Image successfully resized to thumbnail! 🎉"
            }

    # ------------------------------------------------------------------
    # PDF Processing – Extract text from first page 📄
    # ------------------------------------------------------------------
    elif file_type == "pdf":
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            page_count = len(reader.pages)

            if page_count > 0:
                first_page_text = reader.pages[0].extract_text() or "(no text found)"
                processing_result = {
                    "page_count": page_count,
                    "first_page_preview": first_page_text[:100] + "...",
                    "message": "PDF text extracted successfully! 📖"
                }
            else:
                processing_result = {"message": "Empty PDF – no pages to read 😅"}

    # ------------------------------------------------------------------
    # CSV Processing – Load with pandas and show summary 📊
    # ------------------------------------------------------------------
    elif file_type == "csv":
        df = pd.read_csv(file_path)
        processing_result = {
            "row_count": len(df),
            "columns": list(df.columns),
            "sample_first_row": df.head(1).to_dict(orient="records"),
            "message": f"CSV loaded successfully! Found {len(df)} rows 🚀"
        }

    # ------------------------------------------------------------------
    # Success Response – Celebrate with a nice JSON! 🎊
    # ------------------------------------------------------------------
    return JSONResponse({
        "message": "File uploaded and processed successfully! 🎉",
        "filename": file_obj.filename,
        "content_type": file_obj.content_type,
        "description": description,
        "processing_result": processing_result
    })


# ------------------------------------------------------------------
# Bonus Utility Endpoint – Clean up uploaded files (great for demos!)
# Not recommended for production without authentication! ⚠️
# ------------------------------------------------------------------
@app.delete("/cleanup/")
async def cleanup_uploads():
    """
    Deletes all files in the uploads folder.
    Useful when testing locally or running demos.
    """
    try:
       for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)  # Silently continue on error
    except Exception as e:
        print(e)  # Silently continue on error

    return {"message": "All uploaded files have been cleaned! 🧹 Sparkling clean!"}


# ------------------------------------------------------------------
# Run with: uvicorn main:app --reload
# Then visit: http://127.0.0.1:8000/docs for the beautiful interactive API docs!
# ------------------------------------------------------------------