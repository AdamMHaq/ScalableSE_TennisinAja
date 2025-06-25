from fastapi import APIRouter, HTTPException, Depends, Query
from models import CourtIn, CourtOut  
from database import court_collection
from datetime import datetime
from bson.objectid import ObjectId
import httpx
from utils.auth import get_current_user
from typing import Optional

USER_SERVICE_URL = "http://user_service:8000/users"

router = APIRouter()

async def user_exists(user_id: str) -> bool:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{USER_SERVICE_URL}/{user_id}")
            return resp.status_code == 200
        except:
            return False

@router.post("/", response_model=CourtOut)
async def create_court(court: CourtIn, current_user=Depends(get_current_user)):
    if not await user_exists(current_user["sub"]):
        raise HTTPException(status_code=404, detail="User not found")
    
    court_dict = court.dict()
    court_dict["created_by"] = current_user["sub"]
    court_dict["createdAt"] = datetime.utcnow()
    
    result = await court_collection.insert_one(court_dict)
    court_dict["id"] = str(result.inserted_id)
    court_dict.pop("_id", None)  # Remove MongoDB _id field
    
    return CourtOut(**court_dict)

@router.get("/", response_model=list[CourtOut])
async def list_courts(
    limit: int = Query(50, le=100, description="Number of courts to return"),
    skip: int = Query(0, ge=0, description="Number of courts to skip"),
    surface: Optional[str] = Query(None, description="Filter by surface type"),
    is_indoor: Optional[bool] = Query(None, description="Filter by indoor/outdoor")
):
    # Build query filter
    query_filter = {}
    if surface:
        query_filter["surface"] = {"$regex": surface, "$options": "i"}  # Case insensitive
    if is_indoor is not None:
        query_filter["is_indoor"] = is_indoor
    
    # Use pagination and indexing for better performance
    cursor = court_collection.find(query_filter).skip(skip).limit(limit).sort("createdAt", -1)
    courts = []
    
    async for court in cursor:
        court["id"] = str(court["_id"])
        court.pop("_id", None)
        courts.append(CourtOut(**court))
    
    return courts

@router.get("/public", response_model=list[CourtOut])
async def list_courts_public(
    limit: int = Query(50, le=100, description="Number of courts to return"),
    skip: int = Query(0, ge=0, description="Number of courts to skip"),
    surface: Optional[str] = Query(None, description="Filter by surface type"),
    is_indoor: Optional[bool] = Query(None, description="Filter by indoor/outdoor")
):
    """Public endpoint to list courts without authentication"""
    # Build query filter
    query_filter = {}
    if surface:
        query_filter["surface"] = {"$regex": surface, "$options": "i"}  # Case insensitive
    if is_indoor is not None:
        query_filter["is_indoor"] = is_indoor
    
    # Use pagination and indexing for better performance
    cursor = court_collection.find(query_filter).skip(skip).limit(limit).sort("createdAt", -1)
    courts = []
    
    async for court in cursor:
        court["id"] = str(court["_id"])
        court.pop("_id", None)
        courts.append(CourtOut(**court))
    
    return courts

@router.get("/{court_id}", response_model=CourtOut)
async def get_court_by_id(court_id: str):
    try:
        court = await court_collection.find_one({"_id": ObjectId(court_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid court ID format")
    
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")
    
    court["id"] = str(court["_id"])
    court.pop("_id", None)
    
    return CourtOut(**court)

@router.put("/{court_id}", response_model=CourtOut)
async def update_court(court_id: str, court_update: CourtIn, current_user=Depends(get_current_user)):
    try:
        # Check if court exists and user owns it
        existing_court = await court_collection.find_one({"_id": ObjectId(court_id)})
        if not existing_court:
            raise HTTPException(status_code=404, detail="Court not found")
        
        if existing_court["created_by"] != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Not authorized to update this court")
        
        update_data = court_update.dict()
        update_data["updatedAt"] = datetime.utcnow()
        
        result = await court_collection.update_one(
            {"_id": ObjectId(court_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Court not found")
        
        court = await court_collection.find_one({"_id": ObjectId(court_id)})
        court["id"] = str(court["_id"])
        court.pop("_id", None)
        
        return CourtOut(**court)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid court ID format")

@router.delete("/{court_id}")
async def delete_court(court_id: str, current_user=Depends(get_current_user)):
    try:
        # Check if court exists and user owns it
        existing_court = await court_collection.find_one({"_id": ObjectId(court_id)})
        if not existing_court:
            raise HTTPException(status_code=404, detail="Court not found")
        
        if existing_court["created_by"] != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Not authorized to delete this court")
        
        result = await court_collection.delete_one({"_id": ObjectId(court_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Court not found")
        
        return {"detail": "Court deleted successfully"}
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid court ID format")

