from fastapi import FastAPI
from router import users,hotels,foods,ratings,auth,notifications,verification,admin,order
from fastapi.middleware.cors import CORSMiddleware
from services.aps_schedular import start_scheduler
 
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(foods.router)
app.include_router(order.router)
app.include_router(ratings.router)
app.include_router(auth.router)
app.include_router(notifications.router)
app.include_router(verification.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
