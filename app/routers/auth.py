"""
Rotas de autenticação: registro de usuário, login (emissão de token) e perfil.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import authenticate_user, create_access_token, get_current_active_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário. O e-mail deve ser único."""
    existing_user = crud.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário cadastrado com este e-mail",
        )
    return crud.create_user(db, user_in)


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna um token JWT.
    Usa OAuth2PasswordRequestForm: o campo 'username' deve receber o e-mail.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return schemas.Token(access_token=access_token)


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user=Depends(get_current_active_user)):
    """Retorna os dados do usuário autenticado (rota protegida)."""
    return current_user
