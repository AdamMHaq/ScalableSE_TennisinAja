from fastapi import FastAPI
from routers import users

app = FastAPI(
    title="TennisinAja - User Service",
    version="1.0.0"
)

# Register the user-related routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Root route for testing
@app.get("/")
def root():
    return {"message": "Welcome to TennisinAja User Service"}
