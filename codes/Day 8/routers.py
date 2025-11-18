from fastapi import APIRouter
from .utils.hashing import router as hashing_router
from .utils.sanitizer import router as sanitizer_router
from .utils.truncator import router as truncator_router
from .hello import router as hello_router

router = APIRouter()
router.include_router(hello_router,prefix='/welcome')
router.include_router(hashing_router,prefix='/hashing')
router.include_router(sanitizer_router,prefix='/sanitize')
router.include_router(truncator_router,prefix='/truncate')