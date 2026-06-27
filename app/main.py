from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password ='password123', row_factory = dict_row)
    cursor = conn.cursor()
    print("Database connection was successfull!")
except Exception as error:
    print("Connecting to database failed.")
    print("Error:",error)



my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "I like pizza",
        "id": 2
    }
]

@app.get("/")
async def root():
    return {"message": "Hello World"} #path operation / route in other frameowrks

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
             return i


@app.get("/posts")
async def get_posts():
    return {"data" : "this is your post"}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

@app.get("/posts/{id}")
def get_post(id : int, response: Response ):
    #print(id)
    #print(type(id))
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id: {id} was not found"}
    print(post)
    return {"post_detail":post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

app.put("/posts/{id}")
def update_posts(id : int, post = Post):
    print(post)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    my_posts.pop(index)
    return {"data":post_dict}

