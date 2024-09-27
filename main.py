from fastapi import FastAPI
from router import users,hotels,foods,ratings
 
app = FastAPI()

app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(foods.router)
app.include_router(ratings.router)