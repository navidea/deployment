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
import psycopg2.errors 
from psycopg2.extras import RealDictCursor
import time
from time import sleep
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
    except psycopg2.errors.OperationalError as e :
       print("connection to database failed.\nerorr:",e)
       time.sleep(2)


#get
@app.get("/posts/")
def get_posts():
    return {"posts" : my_posts}


#get one 
@app.get("/posts/{id_}",)
def get_post(id_:int,response:Response):
    post = [item for item in my_posts if item["id"]==id_]
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id_} was not found.")
    return {"post":post}


#create
@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post=Body(...)):
    post_new = post.model_dump()
    post_new["id"] = f"{randint(0,1000000)}"
    my_posts.append(post_new)
    return {"posts":my_posts}


#delete 
@app.delete("/posts/{id_}")
def delete_post(id_ : int):
    #find
    post=[my_posts.pop(my_posts.index(item)) for item in my_posts if item["id"]==id_]

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_} was not found.")
    #select
    #return response

    return Response(status_code=status.HTTP_204_NO_CONTENT) 


#update
@app.put("/posts/{id_}")
def update_post(id_:int,post:Post):
   #find post index
   indexes = [my_posts.index(item) for item in my_posts if item["id"]==id_]

   # exception handling
   if not indexes :
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id {id_} not found") 
                          
   index = indexes[0]
   
   post_dict = post.model_dump()
   # put id 
   my_posts[index] = post_dict
   my_posts[index]["id"] = id_
  
   # return response 
   return {"message":f"post with id {indexes[0]} updated"}


