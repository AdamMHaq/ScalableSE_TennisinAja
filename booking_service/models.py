from pydantic import BaseModel
from datetime import datetime

class BookingIn(BaseModel):
    user_id: str
    court_id: str
    time_slot: str  # ISO format
    duration: int  # Duration in hours
    booking_date: datetime  # Date of the booking in ISO format
    booking_by: str  # User ID of the person making the booking
    status: str = "pending"  # Booking status: "pending", "confirmed", "cancelled"
    payment_status: str = "unpaid"  # "unpaid", "paid", "refunded"
    confirmation_code: str = ""     # Unique code for booking confirmation

class BookingOut(BookingIn):
    id: str
    createdAt: datetime
    updated_at: datetime = None