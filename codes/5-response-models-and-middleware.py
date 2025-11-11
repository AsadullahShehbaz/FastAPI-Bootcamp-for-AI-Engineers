from fastapi.responses import JSONResponse
from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
import time 
app = FastAPI()

class QouteIn(BaseModel):
    text:str
    author:str

class QouteOut(BaseModel):
    text:str
    author:str
    id:int

qoutes_db = [
    {"id": 1, "author": "Ayan Ahmed", "text": "Study is the best way to learn anything and everything."},
    {"id": 2, "author": "Muhammad Arsal", "text": "Success is not final, failure is not fatal: It is the courage to continue that counts."},
    {"id": 3, "author": "Hafiz Abdullah", "text": "The only way to do great work is to love what you do."}
]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"The Request Method is {request.method}")
    print(f"The Request URL is {request.url}")
    print(f"The Process Time is {process_time}")
    return response

@app.get('/',response_model=list[QouteOut])
def get_qoutes():
    return qoutes_db
@app.get('/qoutes',response_model=list[QouteOut])
def get_qoutes():
    return qoutes_db

@app.post('/qoutes',response_model=QouteOut)
def create_qoute(qoute:QouteIn):
    new_id = len(qoutes_db)+1
    new_qoute = {'id':new_id,**qoute.model_dump()
    }
    qoutes_db.append(new_qoute)
    return new_qoute

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request:Request,exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error':True,
            'message':exc.detail,
            'hint':'Check your input values again',
            'path':str(request.url)
        }
    )