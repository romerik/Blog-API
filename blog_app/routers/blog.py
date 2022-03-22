from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import BlogBase, ShowBlog
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List

router = APIRouter(
    tags=['Blogs'],
    prefix='/blogs'
)

@router.get("/", response_model=List[ShowBlog])
def get(db: Session = Depends(get_db)):
    blogs  = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", response_model=ShowBlog)
def show(id : int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} is not found")
    
    return blog


@router.post('/{user_id}', response_model=ShowBlog)
def create(user_id, request : BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, is_published=request.is_published, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put("/{id}", response_model=ShowBlog)
def update(id : int, request : BlogBase, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} is not found")

    #blog.update(title=request.title, body=request.body, is_published=request.is_published)
    blog.update(request.dict())
    db.commit()
    #return {"data" : f"Blog with id = {id} updated successfullly"}
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog


@router.delete('/{id}')
def destroy(id : int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} is not found")
    
    blog.delete(synchronize_session=False)
    db.commit()

    return {"data" : f"The blog of id = {id} is deleted"}