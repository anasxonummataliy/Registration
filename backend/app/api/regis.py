from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.database.session import get_db
from app.database.models.user import User

router = APIRouter(
    prefix="/regis",
    tags= ["Registration"]
)

#Parolni berkitish uchun 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    name : str
    email : EmailStr
    password : str

@router.post("/")
async def registration(request : RegisterRequest, db : AsyncSession = Depends(get_db)):
    #Email mavjud ekanini tekshiramiz
    result = await db.execute(select(User).filter(User.email == request.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ro'yhatdan o'tdi.")
    
    #parolni yashirish
    hasheed_password = pwd_context.hash(request.password)

    #yangi user qo'shish
    new_user = User(name=request.name, email=request.email, password = hasheed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message" : "Foydalanuvchi ro'yhatdan o'tdi", "user_id" : new_user.id}