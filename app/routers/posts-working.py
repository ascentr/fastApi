from typing import List, Optional
from fastapi import  Response, status, HTTPException , Depends, APIRouter 
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.functions import current_user, mode
from starlette.status import HTTP_403_FORBIDDEN
from .. import models , schemas , oauth2 
from .. database import  get_db

router = APIRouter(
    prefix="/posts" ,
    tags =["Posts"]
)

#allposts
#@router.get("/" ,  response_model=List[schemas.PostResponse])
@router.get("/" ,  response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), limit_to:int = 10, skip: int = 0 , search: Optional[str] = ''):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit_to).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit_to).offset(skip).all()

    return results

#get all posts by one user
@router.get('/byuser' , response_model=List[schemas.PostResponse])
def get_user_posts(
    db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)): 

    posts_by_user = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts_by_user


#create post
@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#get one post with id
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    print(current_user.id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} WAS NOT FOUND')
        
    return post

#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorised to perform requested action')



    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@router.put("/{id}" , response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorised to perform requested action')

    post_query.update(updated_post.dict())
    db.commit()
 
    return post_query.first() 
