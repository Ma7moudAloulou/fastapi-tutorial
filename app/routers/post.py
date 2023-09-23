from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],  # to regroup posts APIs in /docs so APIs are organised
)


@router.get("/", response_model=List[schemas.PostOut])  # List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts""")
    
    # posts = cursor.fetchall()
    # print(posts)
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.tilte.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(results)

    return results  # posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)  ## !!!!!!!!!!!!!!!!!!!!!!!!! status code in decerator
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()  # when changing the database

    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# title str , content str


# with PUT you have to give all details of objects to update
# with PATCH only the one field to update


@router.get("/{id}", response_model=schemas.Post)  # id is called path parameter
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    
    # print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id= %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()  # when changing the database

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    # check if its the user's post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform the required action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )  ## when status code is 204, fastapi does not except a json return


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts SET title=%s, content=%s, published=%s WHERE id= %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()  # when changing the database

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    # check if its the user's post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform the required action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
