# 404 – Model Not Found
# 422 – Invalid Input
# 500 – Internal Server Error
# 429 – Rate Limiting

from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel , ValidationError
import time 
app = FastAPI(title="AI Model API with Error Handling")

# -----------------------------
# Dummy Model Store
# -----------------------------
AVAILABLE_MODELS = {
    "sentiment": lambda text: "positive" if "good" in text else "negative",
    "length": lambda text: len(text)
}


# -----------------------------
# Rate Limiting (simple demo)
# -----------------------------
RATE_LIMIT_WINDOW = 10  # seconds
RATE_LIMIT_MAX_REQUESTS = 5

user_request_log = {}

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    logs = user_request_log.get(ip,[])
    logs = [t for t in logs if now-t < RATE_LIMIT_WINDOW]
    user_request_log[ip] = logs 

    if len(logs)>RATE_LIMIT_MAX_REQUESTS:
        return True 
    logs.append(now)
    return False 

class PredictRequest(BaseModel):
    text : str 


@app.exception_handler(ValidationError)
async def validation_exception_handler(request : Request , exc : ValidationError):
    return JSONResponse(status_code= 422, content = {'error':'Invalid Input','detail':exc.errors()})

@app.exception_handler(Exception)
async def internal_exception_handler(request : Request,exc : Exception):
    return JSONResponse(status_code=500,content={'error':'Internal Server Error','message':str(exc)})

# api rou
@app.post("/predict/{model_name}")
async def predict(
    model_name : str,
    payload : PredictRequest,
    request : Request
):
    # rate limiting check 
    client_ip = request.client.host 
    if is_rate_limited(client_ip):
        return HTTPException(status_code=429,detail='Too many requests,please try later!')

    if model_name not in AVAILABLE_MODELS:
        raise HTTPException(status_code=404,detail=f'Model {model_name} not found')
    try : 
        model_fn = AVAILABLE_MODELS[model_name]
        result = model_fn(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Model Execution Failed : {str(e)}")
    return {'model':model_name,'input':payload.text,'result':result}