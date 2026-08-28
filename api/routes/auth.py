from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database.postgres import get_db
from services.auth_service import AuthService

router = APIRouter(
    prefix = "/auth",
    tags=["Authentication"]
)

# --------------------------------------------------
# Request body(schema)
# --------------------------------------------------
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --------------------------------------------------
# Register the form of new user
# --------------------------------------------------
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register (
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    try:
        user = AuthService.register_user(
            db=db,
            full_name=request.full_name,
            email=request.email,
            password=request.password
        )
        return{
            "message":"User registered successfully.",
            "user":{
                "id": user.id,
                "full_name": user.full_name,
                "email":user.email
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# --------------------------------------------------
# User Login details
# --------------------------------------------------
@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate the user and also returns the jwt token for that particular user
    """
    try:
        result = AuthService.login_user(
            db=db,
            email=request.email,
            password=request.password
        )
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTPS_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
            "WWW-Authenticate": "Bearer"
            }
        )