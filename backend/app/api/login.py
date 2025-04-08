import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.database.session import get_db
from app.database.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post('/')
async def login(request: LoginRequest,
                db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning(
            f"Bunday email bilan ro'yhatdan o'tilmagan : {request.email}")
        raise HTTPException(
            status_code=404, detail="Bu email ro'yhatdan o'tmagan. Iltimos ro'yhatdan o'ting. ")

    try:
        if ph.verify(user.password, request.password):
            logger.info(f"User logged in successfully: {user.email} ")
            return {
                "message": "Tizimga muvaffaqiyatli kirdingiz",
                "user_id": user.id,
                "name": user.name
            }
    except VerificationError:
        logger.warning(f"Invalid password for email: {request.email}")
        raise HTTPException(status_code=401, detail="Parol noto'g'ri.")
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Parolni tekshirishda xatolik yuz berdi.")
