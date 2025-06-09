from fastapi import FastAPI
from routers import bookings

app = FastAPI(
    title="TennisinAja - Booking Service",
    version="1.0.0"
)

app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

@app.get("/")
def root():
    return {"message": "Welcome to TennisinAja Booking Service"}