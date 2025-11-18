from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def welcome():
    return {'Message':'Welcome to AI Engineer Utils Tutorial','Content':'Hashing,URL Sanitization,Safe text truncation,Logging (info & error logging)'}