# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: learning_deployment
#     language: python
#     name: python3
# ---

from typing import List
from time import time
from fastapi import Depends, FastAPI, Body,Response,HTTPException,status
from psycopg2 import connect
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from db.database import Base, engine, get_db
from db import model 
from schema import schema

app = FastAPI()
Base.metadata.create_all(bind=engine)

while True:
    try:
        conn =connect(user="user_test", password="123456",database="fastapi",
                                host="localhost", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection to database successfully.")
        break
    except OperationalError as e :
       print("connection to database failed.\nerorr:",e)
       time.sleep(2)


#get 
@app.get("/posts/",response_model=List[schema.Post])
def get_posts(db: Session=Depends(get_db)):
   posts = db.query(model.Post).all()
   return posts


#get one 
@app.get("/posts/{id_}",response_model=schema.Post)
def get_post(id_:int,response:Response,db: Session=Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id_).first()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} was not found.")
    return post


#create
@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_posts(post:schema.PostCreate=Body(...),db:
                  Session=Depends(get_db))->schema.Post:
    post_dict = post.model_dump()
    post_created = model.Post(**post_dict)
    db.add(post_created)
    db.commit()
    db.refresh(post_created)
    return post_created


#delete 
@app.delete("/posts/{id_}")
def delete_post(id_ : int,db : Session=Depends(get_db)):
    post_deleted = db.query(model.Post).filter(model.Post.id == id_).first()
    # post_deleted = post_delete_query.first()
    if not post_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} was not found.")
    # post_delete_query.delete(synchronize_session=False)
    db.delete(post_deleted)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


#update
@app.put("/posts/{id_}")
def update_post(id_:int,post_updated:schema.PostCreate, db : Session = Depends(get_db))->schema.Post:
    #find post index
    post_update_query = db.query(model.Post).filter(model.Post.id==id_)
    post = post_update_query.first()
    # exception handling
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} not found") 
    post_update_query.update(post_updated.model_dump())
    db.commit()
    db.refresh(post)
    return post 
