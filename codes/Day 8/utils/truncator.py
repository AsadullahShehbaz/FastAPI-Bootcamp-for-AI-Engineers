from fastapi import APIRouter

router = APIRouter()

def safe_truncate(text:str,max_length:int,suffix:str='...')->str:
    if len(text)<=max_length:
        return text
    
    truncated_text = text[:max_length].rsplit(" ",1)[0]
    final_text = truncated_text + suffix
    return final_text

@router.get('/truncate')
async def truncate_text(text:str,max_length:int=30):
    result = safe_truncate(text)
    return {
        'Real Text ':text,
        'Truncated Text ':truncate_text
    }