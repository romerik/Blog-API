from fastapi import FastAPI
from blog_app.routers import blog, user, authentication
from blog_app import models
from blog_app.database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)