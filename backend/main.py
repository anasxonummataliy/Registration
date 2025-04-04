from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

users = []

@app.post("/")
async def create_user():
    pass