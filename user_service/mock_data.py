from datetime import datetime
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Mock user data
MOCK_USERS = [
    {
        "_id": ObjectId(),
        "name": "Admin User",
        "email": "admin@tennisinaja.com",
        "role": "admin",
        "password": hash_password("admin123"),
        "createdAt": datetime.now()
    },
    {
        "_id": ObjectId(),
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "player",
        "password": hash_password("player123"),
        "createdAt": datetime.now()
    },
    {
        "_id": ObjectId(),
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "role": "player",
        "password": hash_password("player123"),
        "createdAt": datetime.now()
    },
    {
        "_id": ObjectId(),
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "role": "player",
        "password": hash_password("player123"),
        "createdAt": datetime.now()
    },
    {
        "_id": ObjectId(),
        "name": "Sarah Wilson",
        "email": "sarah.wilson@example.com",
        "role": "player",
        "password": hash_password("player123"),
        "createdAt": datetime.now()
    }
]
