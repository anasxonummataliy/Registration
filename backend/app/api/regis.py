from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from argon2 import PasswordHasher
from argon2.exceptions import HashingError
from app.database.session import get_db
from app.database.models.user import User
import logging


router = APIRouter(
    prefix="/regis",
    tags=["Registration"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ph = PasswordHasher()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


@router.post("/")
async def registration(request: RegisterRequest, db: AsyncSession = Depends(get_db)):

    async with db.begin():
        stmt = select(User).where(User.email == request.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning(f"Email already registered: {request.email}")
            raise HTTPException(
                status_code=400, detail="Bu email allaqachon ro‘yxatdan o‘tgan.")

        try:
            hasheed_password = ph.hash(request.password)
        except HashingError as e:
            logger.error(f"Failed to hash password: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Parolni hash qilishda xatolik yuz berdi.")

        # yangi user qo'shish
        new_user = User(
            name=request.name,
            email=request.email,
            password=hasheed_password
        )
        db.add(new_user)
    try:
        await db.commit()
        new_user = (await db.execute(select(User).where(User.id == new_user.id))).scalar_one_or_none()
        if not new_user:
            raise HTTPException(
                status_code=500, detail="Foydalanuvchi topilmadi.")
    except Exception as e:
        logger.error(f"Failed to save user to database: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Foydalanuvchini saqlashda xatolik yuz berdi.")

    logger.info(
        f"User registered successfully: {new_user.email}, ID: {new_user.id}")
    return {"message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi", "user_id": new_user.id}
