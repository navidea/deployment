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

# +
from random import randint
from typing import Optional
from fastapi import FastAPI,status,Response,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
import psycopg2 
from psycopg2.errors import OperationalError
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
class Post(BaseModel):
    title : str
    content : str 
    is_published : bool = True

my_posts =[
    {  
        "id" : 1,                       
        "title" : "first post",
        "content" : "this is my first post."
    },
    {
        "id" : 2,
        "title" : "second post",
        "content" : "this is my second post."
    }
]        

# -

while True:
    try:
        conn = psycopg2.connect(user="user_test", password="123456",database="fastapi",
                                host="localhost", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection to database successfully.")
        break
    except OperationalError as e :
       print("connection to database failed.\nerorr:",e)
       time.sleep(2)


#get
@app.get("/posts/")
def get_posts():
    conn.cursor("""SELECT * FROM post;""")
    posts = cursor.fetchall()
    return {"data" : posts}


#get one 
@app.get("/posts/{id_}",)
def get_post(id_:int,response:Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""",(str(id_),))
    post = cursor.fetchone()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} was not found.")
    return {"post":post}


#create
@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post=Body(...)):
    post_dict = post.model_dump()
    cursor.execute("""INSERT INTO post (title, content, published)
                    VALUES(%s, %s, %s) RETURNING *; """,
                    (post.title, post.content, post.is_published))
    post_ret = cursor.fetchone()
    conn.commit()
    return {"posts":post_ret}


#delete 
@app.delete("/posts/{id_}")
def delete_post(id_ : int):
    #find
    cursor.execute("""DELETE FROM post WHERE id = %s Returning *;""",(str(id_),))
    conn.commit()
    post_deleted = cursor.fetchone()
    if not post_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} was not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


#update
@app.put("/posts/{id_}")
def update_post(id_:int,post:Post):
   #find post index
   cursor.execute("""UPDATE post SET title = %s, content=%s, published=%s WHERE id = %s RETURNING * """
                  ,(post.title, post.content, post.is_published,str(id_)))

   post_updated = cursor.fetchone()
   conn.commit()
   # exception handling
   if not post_updated :
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id {id_} not found") 
   # return response 
   return {"updated post :":post_updated}


