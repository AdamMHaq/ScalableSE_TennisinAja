import asyncio
from database import booking_collection, insert_mock_data

async def reset_bookings():
    # Clear existing bookings
    await booking_collection.delete_many({})
    print("Existing bookings cleared")
    
    # Insert new mock data
    await insert_mock_data()

asyncio.run(reset_bookings())
