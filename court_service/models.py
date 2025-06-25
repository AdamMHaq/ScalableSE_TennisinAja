from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourtIn(BaseModel):
    name: str
    contact_phone: str  # Contact phone number
    address: str
    gmaps_link: str  # Google Maps link for the court
    surface: str  # e.g., "clay", "grass", "hard"
    is_indoor: bool
    price_per_hour: float  # Price in local currency
    available_days: list[str]  # List of available time slots in ISO format
    available_courts: int  # Number of courts available for booking

class CourtOut(CourtIn):
    id: str
    created_by: str  # User ID of the creator
    createdAt: datetime