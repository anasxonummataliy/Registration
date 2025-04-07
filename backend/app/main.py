import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]

)

class User(BaseModel):
    name : str
    email : str
    password : str

 
@app.post("/registration")
async def create_account(
    user : User
):
    file_path = Path("users.json")
    if file_path.exists():
        with open(file_path, 'r', encoding="utf-8") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else :
        users = []
    
    users.append(user.dict())

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return {"message" : "User saved to Json file", "user" : user}


