<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from database import get_database

router = APIRouter()

async def get_collection():
    db = await get_database()
    return db.bookings

@router.get("/")
async def get_bookings(collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        bookings = await collection.find().to_list(1000)
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_booking(booking: dict, collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        result = await collection.insert_one(booking)
        if result.inserted_id:
            return {"message": "Booking created successfully", "booking_id": str(result.inserted_id)}
        raise HTTPException(status_code=400, detail="Failed to create booking")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
from fastapi import APIRouter, HTTPException, Body, Depends
from utils.auth import get_current_user
from models import BookingIn, BookingOut
from database import booking_collection
from datetime import datetime
from bson.objectid import ObjectId
import httpx

COURT_SERVICE_URL = "http://127.0.0.1:8001/courts"

router = APIRouter()

async def court_exists(court_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{COURT_SERVICE_URL}/{court_id}")
        return resp.status_code == 200

@router.post("/", response_model=BookingOut)
async def create_booking(booking: BookingIn):
    if not await court_exists(booking.court_id):
        raise HTTPException(status_code=404, detail="Court not found")

    exists = await booking_collection.find_one({
        "court_id": booking.court_id,
        "time_slot": booking.time_slot
    })
    if exists:
        raise HTTPException(status_code=400, detail="Court already booked for this time slot")

    booking_dict = booking.dict()
    now = datetime.utcnow()
    booking_dict["createdAt"] = now
    booking_dict["updated_at"] = now  # Set updated_at on creation
    result = await booking_collection.insert_one(booking_dict)
    booking_dict["id"] = str(result.inserted_id)
    return BookingOut(**booking_dict)

@router.get("/", response_model=list[BookingOut])
async def list_bookings():
    bookings = []
    async for booking in booking_collection.find():
        booking["id"] = str(booking["_id"])
        bookings.append(BookingOut(**booking))
    return bookings

@router.put("/{booking_id}", response_model=BookingOut)
async def update_booking(booking_id: str, booking_update: BookingIn, current_user=Depends(get_current_user)):
    booking = await booking_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    # Only owner or admin can update
    if booking["user_id"] != current_user["sub"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = booking_update.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await booking_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": update_data}
    )
    booking = await booking_collection.find_one({"_id": ObjectId(booking_id)})
    booking["id"] = str(booking["_id"])
    return BookingOut(**booking)

@router.delete("/{booking_id}")
async def delete_booking(booking_id: str, current_user=Depends(get_current_user)):
    booking = await booking_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    # Only owner or admin can delete
    if booking["user_id"] != current_user["sub"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await booking_collection.delete_one({"_id": ObjectId(booking_id)})
    return {"detail": "Booking deleted"}

@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking_by_id(booking_id: str, current_user=Depends(get_current_user)):
    booking = await booking_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    # Only owner or admin can view
    if booking["user_id"] != current_user["sub"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    booking["id"] = str(booking["_id"])
    return BookingOut(**booking)

@router.get("/user/{user_id}", response_model=list[BookingOut])
async def list_bookings_by_user(user_id: str):
    bookings = []
    async for booking in booking_collection.find({"user_id": user_id}):
        booking["id"] = str(booking["_id"])
        bookings.append(BookingOut(**booking))
    return bookings

@router.get("/court/{court_id}", response_model=list[BookingOut])
async def list_bookings_by_court(court_id: str):
    bookings = []
    async for booking in booking_collection.find({"court_id": court_id}):
        booking["id"] = str(booking["_id"])
        bookings.append(BookingOut(**booking))
    return bookings

@router.patch("/{booking_id}/status", response_model=BookingOut)
async def change_booking_status(booking_id: str, status: str = Body(...), current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can change status")
    result = await booking_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking = await booking_collection.find_one({"_id": ObjectId(booking_id)})
    booking["id"] = str(booking["_id"])
    return BookingOut(**booking)
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
