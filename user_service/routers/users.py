<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from database import get_database

router = APIRouter()

async def get_collection():
    db = await get_database()
    return db.users

@router.get("/")
async def get_users(collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        users = await collection.find().to_list(1000)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        user = await collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
from fastapi import APIRouter, HTTPException, Depends, Header
from models import UserIn, UserOut
from auth import hash_password, verify_password, create_access_token, decode_access_token
from database import user_collection  # Note: should be user_collection, not users_collection
from bson.objectid import ObjectId
from datetime import datetime
from jose import JWTError
from models import LoginRequest

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserIn):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["createdAt"] = datetime.utcnow()
    result = await user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserOut(**user_dict)

@router.post("/login")
async def login(login_req: LoginRequest):
    user = await user_collection.find_one({"email": login_req.email})
    if not user or not verify_password(login_req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.get("/me", response_model=UserOut)
async def get_me(current=Depends(get_current_user)):
    user_id = current["sub"]
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return UserOut(**user)

@router.get("/", response_model=list[UserOut])
async def list_users():
    users = []
    async for user in user_collection.find():
        user["id"] = str(user["_id"])
        users.append(UserOut(**user))
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return UserOut(**user)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_update: UserIn, current_user=Depends(get_current_user)):
    # Only owner or admin can update
    if user_id != current_user["sub"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = user_update.dict()
    update_data["password"] = hash_password(update_data["password"])
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    user["id"] = str(user["_id"])
    return UserOut(**user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user=Depends(get_current_user)):
    # Only owner or admin can delete
    if user_id != current_user["sub"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
