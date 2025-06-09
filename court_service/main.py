from fastapi import FastAPI
from routers import courts

app = FastAPI(
    title="TennisinAja - Court Service",
    version="1.0.0"
)

app.include_router(courts.router, prefix="/courts", tags=["Courts"])

@app.get("/")
def root():
    return {"message": "Welcome to TennisinAja Court Service"}