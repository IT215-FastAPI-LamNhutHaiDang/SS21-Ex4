from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import jwt

router = APIRouter()

class LoginRequest:
    email: str
    password: str

class User:
    email: str
    password: str
    role: str

def get_db():
    pass

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        return {
            "success": False,
            "message": "Email không tồn tại"
        }

    if data.password != user.password:
        return {
            "success": False,
            "message": "Mật khẩu không chính xác"
        }

    token = jwt.encode(
        {
            "email": user.email,
            "password": user.password,
            "role": user.role
        },
        "123456",
        algorithm="HS256"
    )

    return {
        "success": True,
        "access_token": token
    }
