from fastapi import APIRouter
from typing import Optional
from urllib.parse import urlparse

router = APIRouter()

def safe_url_sanitizer(url:str)->Optional[str]:
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme in ('http','https') and parsed_url.netloc:
            return url
    except Exception as e:
        pass
    print(f"Unsafe URL Detected: {url}")
    return None

@router.get('/sanitize_url')
async def sanitize(url:str):
    sanitized_url = safe_url_sanitizer(url)
    return {
        'Main URL':url,
        'Sanitized URL':sanitized_url
    }


