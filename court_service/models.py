from pydantic import BaseModel
from datetime import datetime

class CourtIn(BaseModel):
    name: str
    contact_phone: str  # Contact phone number
    address: str
    gmaps_link: str  # Google Maps link for the court
    surface: str  # e.g., "clay", "grass", "hard"
    is_indoor: bool
    price_per_hour: float  # Price in local currency
    available_days: list[str]  # List of available time slots in ISO format (e.g., "2023-10-01T10:00:00Z")
    available_courts: int  # Number of courts available for booking
    created_by: str  # User ID of the creator

class CourtOut(CourtIn):
    id: str
    createdAt: datetime