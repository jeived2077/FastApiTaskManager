import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Импорт для CORS
import  Route.Comment_Route as Comment_Route
import Route.Project_Route as Project_Route
import Route.Task_Route as Task_Route
import Route.Auth_Route as Auth_Route
from Route import Email_Route

load_dotenv(dotenv_path='env/.env')
print("Loaded Environment Variables:")
print(f"ALGORITHM: {os.getenv('ALGORITHM')}")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"REFRESH_SECRET_KEY: {os.getenv('REFRESH_SECRET_KEY')}")
print(f"HOST_API: {os.getenv('HOST_API')}")
print(f"PORT_API: {os.getenv('PORT_API')}")
print("-" * 30)
app = FastAPI ( )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(Email_Route.router)
app.include_router(Comment_Route.router)
app.include_router(Project_Route.router)
app.include_router(Task_Route.router)
app.include_router(Auth_Route.router)

