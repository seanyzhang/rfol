from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter

import app.models as models
from app.db import engine
from app.logger import logger
from app.redis import redis_client

from app.users.routes import router as user_router
from app.auth.routes import router as auth_router
from app.sessions.routes import router as session_router

async def custom_callback(request, response, pexpire):
    """
    Custom callback for rate limiting.

    Args:
        request: The incoming request.
        response: The response to be sent.
        pexpire: The expiration time for the rate limit.
    """
    logger.warning("Rate limit exceeded")
    response.status_code = 429
    response.body = b'{"detail":"Too many requests. Try again later."}'
    response.headers["Content-Type"] = "application/json"

async def identifier(request):
    """
    Custom identifier function for rate limiting.

    Args:
        request: The incoming request.

    Returns:
        str: The identifier for the request, typically the client's host.
    """
    return request.client.host

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan event handler for FastAPI to initialize and close the rate limiter.
    
    Args:
        _: The FastAPI application instance.
    """
    await FastAPILimiter.init(
        redis=redis_client,
        identifier=identifier,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()

# Create FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

# Configure CORS middleware
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

# Initialize the database
models.Base.metadata.drop_all(bind=engine) # CLEAR DB WHILE DEVELOPING TODO REMOVE DURING PRODUCTION
models.Base.metadata.create_all(bind=engine) 

# Include routers for different modules
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(session_router)

# Root endpoint
@app.get("/")
async def root():
    logger.info("startup successful")
    return {"message": "Hello World"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: A message indicating the service is healthy.
    """
    return {"message": "Service is healthy"}