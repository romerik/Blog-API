from fastapi import APIRouter, Depends
from ..database import get_db
from ..schemas import ShowUser, User
from sqlalchemy.orm import Session
from .. import models
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get('/', response_model=List[ShowUser])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

@router.post('/', response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
