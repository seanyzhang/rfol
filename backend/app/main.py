from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter

import app.models as models
from app.db import engine
from app.logger import logger
from app.redis import redis_client

# Router Imports
from app.users.routes import router as user_router
from app.auth.routes import router as auth_router
from app.sessions.routes import router as session_router

async def custom_callback(request, response, pexpire):
    logger.warning("Rate limit exceeded")
    response.status_code = 429
    response.body = b'{"detail":"Too many requests. Try again later."}'
    response.headers["Content-Type"] = "application/json"

async def identifier(request):
    return request.client.host

@asynccontextmanager
async def lifespan(_: FastAPI):
    await FastAPILimiter.init(
        redis=redis_client,
        identifier=identifier,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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
app.include_router(session_router)

@app.get("/")
async def root():
    logger.info("startup successful")
    return {"message": "Hello World"}