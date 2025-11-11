# Import required libraries
import json                # For reading and writing JSON files
import os                  # For file path and existence checking
from typing import Literal, Optional  # For strict type checking in function parameters and models
from uuid import uuid4     # For generating unique IDs for books
from fastapi import FastAPI, HTTPException  # FastAPI framework and HTTP error handling
import random              # For selecting random books
from fastapi.encoders import jsonable_encoder  # Converts Python objects to JSON serializable format
from pydantic import BaseModel  # For creating data models with validation
from mangum import Mangum  # AWS Lambda adapter for FastAPI apps

# Define a Book model for data validation and structure
class Book(BaseModel):
    name: str  # Book title
    genre: Literal["fiction", "non-fiction"]  # Allowed values: "fiction" or "non-fiction"
    price: float  # Price of the book
    book_id: Optional[str] = uuid4().hex  # Optional unique ID (auto-generated if not provided)

# File to store all books in JSON format
BOOKS_FILE = "books.json"
BOOKS = []  # List to store books in memory

# Load existing books from file if available
if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

# Create FastAPI app instance
app = FastAPI()

# Mangum handler to run FastAPI on AWS Lambda
handler = Mangum(app)

# Root endpoint - returns welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}

# Endpoint to get a random book from the store
@app.get("/random-book")
async def random_book():
    return random.choice(BOOKS)

# Endpoint to list all available books
@app.get("/list-books")
async def list_books():
    return {"books": BOOKS}

# Endpoint to get a book by its position in the list
@app.get("/book_by_index/{index}")
async def book_by_index(index: int):
    if index < len(BOOKS):
        return BOOKS[index]
    else:
        # Raise 404 error if index is out of range
        raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")

# Endpoint to add a new book to the store
@app.post("/add-book")
async def add_book(book: Book):
    # Generate a new unique ID for the book
    book.book_id = uuid4().hex
    
    # Convert Pydantic model to JSON-serializable format
    json_book = jsonable_encoder(book)
    
    # Add book to in-memory list
    BOOKS.append(json_book)

    # Save updated book list to file
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)

    # Return the new book's ID
    return {"book_id": book.book_id}
