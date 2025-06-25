from datetime import datetime, timedelta
from bson import ObjectId
import secrets
import string

def generate_confirmation_code(length=8):
    """Generate a random confirmation code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# Mock booking data
MOCK_BOOKINGS = [
    {
        "_id": ObjectId(),
        "user_id": "demo_user",
        "court_id": "6859eeaf5ec62acf2a7397c6",  # Central Tennis Club
        "time_slot": "09:00",
        "duration": 2,
        "booking_date": datetime.now() + timedelta(days=1),
        "booking_by": "demo_user",
        "status": "confirmed",
        "payment_status": "paid",
        "confirmation_code": generate_confirmation_code(),
        "createdAt": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "_id": ObjectId(),
        "user_id": "demo_user",
        "court_id": "6859eeaf5ec62acf2a7397c7",  # Elite Sports Arena
        "time_slot": "14:00",
        "duration": 1,
        "booking_date": datetime.now() + timedelta(days=2),
        "booking_by": "demo_user",
        "status": "confirmed",
        "payment_status": "paid",
        "confirmation_code": generate_confirmation_code(),
        "createdAt": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "_id": ObjectId(),
        "user_id": "demo_user",
        "court_id": "6859eeaf5ec62acf2a7397c8",  # Green Valley Tennis Center
        "time_slot": "16:00",
        "duration": 2,
        "booking_date": datetime.now() + timedelta(days=3),
        "booking_by": "demo_user",
        "status": "pending",
        "payment_status": "unpaid",
        "confirmation_code": generate_confirmation_code(),
        "createdAt": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "_id": ObjectId(),
        "user_id": "demo_user",
        "court_id": "6859eeaf5ec62acf2a7397c9",  # Sunrise Tennis Courts
        "time_slot": "10:00",
        "duration": 1,
        "booking_date": datetime.now() + timedelta(days=4),
        "booking_by": "demo_user",
        "status": "confirmed",
        "payment_status": "paid",
        "confirmation_code": generate_confirmation_code(),
        "createdAt": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "_id": ObjectId(),
        "user_id": "demo_user",
        "court_id": "6859eeaf5ec62acf2a7397ca",  # Riverside Tennis Club
        "time_slot": "18:00",
        "duration": 2,
        "booking_date": datetime.now() + timedelta(days=5),
        "booking_by": "demo_user",
        "status": "cancelled",
        "payment_status": "refunded",
        "confirmation_code": generate_confirmation_code(),
        "createdAt": datetime.now(),
        "updated_at": datetime.now()
    }
]
