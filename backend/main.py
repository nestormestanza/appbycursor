from fastapi import FastAPI
from routers import user, vehicle

app = FastAPI()

app.include_router(user.router)
app.include_router(vehicle.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TLC Vehicle Monitoring API"}