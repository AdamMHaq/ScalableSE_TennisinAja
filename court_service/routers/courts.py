from fastapi import APIRouter, HTTPException, Depends
from models import CourtIn, CourtOut
from database import court_collection
from datetime import datetime
from bson.objectid import ObjectId
import httpx
from utils.auth import get_current_user

USER_SERVICE_URL = "http://127.0.0.1:8000/users"

router = APIRouter()

async def user_exists(user_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{USER_SERVICE_URL}/{user_id}")
        return resp.status_code == 200

@router.post("/", response_model=CourtOut)
async def create_court(court: CourtIn, current_user=Depends(get_current_user)):
    if not await user_exists(current_user["sub"]):
        raise HTTPException(status_code=404, detail="User not found")
    court_dict = court.dict()
    court_dict["created_by"] = current_user["sub"]
    court_dict["createdAt"] = datetime.utcnow()
    result = await court_collection.insert_one(court_dict)
    court_dict["id"] = str(result.inserted_id)
    return CourtOut(**court_dict)

@router.get("/", response_model=list[CourtOut])
async def list_courts():
    courts = []
    async for court in court_collection.find():
        court["id"] = str(court["_id"])
        courts.append(CourtOut(**court))
    return courts

@router.get("/{court_id}", response_model=CourtOut)
async def get_court_by_id(court_id: str):
    court = await court_collection.find_one({"_id": ObjectId(court_id)})
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")
    court["id"] = str(court["_id"])
    return CourtOut(**court)

@router.put("/{court_id}", response_model=CourtOut)
async def update_court(court_id: str, court_update: CourtIn):
    update_data = court_update.dict()
    result = await court_collection.update_one(
        {"_id": ObjectId(court_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Court not found")
    court = await court_collection.find_one({"_id": ObjectId(court_id)})
    court["id"] = str(court["_id"])
    return CourtOut(**court)

@router.delete("/{court_id}")
async def delete_court(court_id: str):
    result = await court_collection.delete_one({"_id": ObjectId(court_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Court not found")
    return {"detail": "Court deleted"}