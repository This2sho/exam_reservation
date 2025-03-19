from fastapi import FastAPI
from app.database.database import engine, Base
from app.router.ReservationRouter import router as reservation_router
from app.router.AuthRouter import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reservation API", version="1.0")

app.include_router(reservation_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"message": "Reservation API is running 🚀"}

