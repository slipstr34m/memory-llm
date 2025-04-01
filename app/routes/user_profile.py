from fastapi import APIRouter
from app.redis_client import redis_client

router = APIRouter()

@router.get("/user-profile/{user_id}")
async def get_user_profile(user_id: str):
    cached_profile = redis_client.get(f"user_timeline:{user_id}")
    
    if cached_profile:
        return {"user_id": user_id, "profile": cached_profile}
    else:
        return {"user_id": user_id, "profile": "No user profile exists."}
