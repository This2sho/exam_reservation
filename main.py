from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
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

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
