from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserIn(BaseModel):
    name: str
    email: EmailStr
    role: str  # 'player' or 'admin'
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    createdAt: datetime

class LoginRequest(BaseModel):
    email: str
    password: str