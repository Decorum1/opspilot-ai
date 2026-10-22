
from fastapi.security import OAuth2PasswordRequestForm 
from fastapi import APIRouter, Depends, HTTPException, status
from auth_dependencies import get_current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from auth_dependencies import require_roles

import models
from database import get_db
from schemas import UserRegister, UserResponse
from security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    email = str(user.email).strip().lower()

    existing_user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = models.User(
        full_name=user.full_name.strip(),
        email=email,
        hashed_password=hash_password(user.password),
        role="viewer",
        is_active=True
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username.strip().lower()

    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if (
        user is None
        or not verify_password(
            form_data.password,
            user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is disabled"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: models.User = Depends(get_current_user)
):
    return current_user


@router.get("/admin-check")
def admin_check(
    current_user: models.User = Depends(
        require_roles("admin")
    )
):
    return {
        "message": "Admin access granted",
        "user": current_user.email,
        "role": current_user.role
    }





