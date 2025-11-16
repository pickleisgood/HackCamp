"""
Health check and status routes
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def status():
    """Get API status"""
    return {"status": "operational"}

@router.get("/version")
async def version():
    """Get API version"""
    return {"version": "0.1.0"}
