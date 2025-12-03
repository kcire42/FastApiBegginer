from fastapi import APIRouter
from app.database.databaseConnection import getDB
import datetime

general_router = APIRouter() # routeur para la API general

# API generica y no tiene conexion con la base de datos

@general_router.get("/")
async def read_root():
    return {"Message": "World"}


@general_router.get("/health")
async def health_check():
    return {"status": "ok"}

@general_router.get("/hour/{format}")
async def get_hour(format: int):
    formatTime = "%I:%M %p"
    if format == 24:
        formatTime = "%H:%M"    
    current_hour = datetime.datetime.now().time().strftime(formatTime)
    return {"current_hour": current_hour}

rank = {
    'S':'Sanin',
    'A':'Jounin',
    'B':'Chunin',
    'C':'Genin',
    'D':'Academy Student'
}

@general_router.get("/name/{name}/{years}/{rank_code}")
async def greet_name(name: str, years: int, rank_code: str):
    rank_full = rank.get(rank_code.upper(), "Unknown Rank")
    return {"greeting": f"Hello, {name}! You are {years} years old and your rank is {rank_full}."}















