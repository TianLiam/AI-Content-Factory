from fastapi import APIRouter

from .signals import router as signals_router
from .materials import router as materials_router
from .contents import router as contents_router
from .ai import router as ai_router

router = APIRouter()

router.include_router(signals_router, prefix="/signals", tags=["Signals"])
router.include_router(materials_router, prefix="/materials", tags=["Materials"])
router.include_router(contents_router, prefix="/contents", tags=["Contents"])
router.include_router(ai_router, prefix="/ai", tags=["AI"])

__all__ = ["router"]
