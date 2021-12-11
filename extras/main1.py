from typing import Optional , List
from fastapi import FastAPI, Response, responses, status, HTTPException , Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models , schemas , utils
from .database import engine , get_db

# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#moved to schemas.py
# class Post(BaseModel):
#     title  : str
#     content : str
#     published : bool = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', 
            user='postgres', password='amjad')

        cursor = conn.cursor()
        print("Succeffully connected to database")
        break                

    except Exception as error:
        print("Could Not Connect - Error :" , error)
        time.sleep(2)

    my_posts = [
        {"title": "Post One", "content":"My First Post, content for FastApi", "id":1 },
        {"title": "Favourite Foods", "content":"Smash Burgers, Grilled Chicken Wings ", "id":2}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p  in enumerate(my_posts):
        if p['id'] == id:
            return i


#sqlAlchemy Routes for Testing
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


#home page
@app.get("/")
def root():
    return ("Hello World")

#allposts
@app.get("/posts" , response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts

#create post
@app.post("/posts" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#get one post with id
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} WAS NOT FOUND')
        
    return post

#delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@app.put("/posts/{id}" , response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first() 


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    #hash the password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}" , response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')

    return user
    
