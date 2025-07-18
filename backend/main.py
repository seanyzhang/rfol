from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
from app.db import engine

# Router Imports
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}