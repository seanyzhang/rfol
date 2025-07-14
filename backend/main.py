from fastapi import FastAPI
import backend.models as models
from backend.db import engine

# Router Imports
from backend.routes.user_routes import router as user_router
from backend.routes.auth_routes import router as auth_router

app = FastAPI()
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}