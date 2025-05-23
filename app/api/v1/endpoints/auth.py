from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.schemas.user import User, UserCreate, Token
from app.services.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user
)
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM accounts WHERE email = %s", (user.email,))
            if cur.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            hashed_password = get_password_hash(user.password)
            cur.execute(
                "INSERT INTO accounts(account_name, email, password) VALUES (%s, %s, %s) RETURNING account_id",
                (user.account_name, user.email, hashed_password)
            )
            account_id = cur.fetchone()[0]
            conn.commit()
            
            return User(
                account_id=account_id,
                account_name=user.account_name,
                email=user.email
            )

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"} 