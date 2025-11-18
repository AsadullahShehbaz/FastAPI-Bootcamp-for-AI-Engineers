from fastapi import FastAPI
from .routers import router as api_router

app = FastAPI(title='Hashing Demo')

app.include_router(api_router)




