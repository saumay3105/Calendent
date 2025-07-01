from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router
import asyncio
import httpx
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_URL = os.getenv("SERVICE_URL", "https://calendent.onrender.com")
PING_INTERVAL = 300
def create_app() -> FastAPI:
    app = FastAPI(title="Calendar Assistant API", version="1.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(chat_router, prefix="/api")
    
    return app

app = create_app()

async def keep_alive_ping():
    """Background task to ping the service every 14 minutes"""
    while True:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{SERVICE_URL}/api/health")
                logger.info(f"Keep-alive ping: {response.status_code}")
        except Exception as e:
            logger.error(f"Keep-alive ping failed: {e}")
        
        await asyncio.sleep(PING_INTERVAL)

@app.get("/")
async def root():
    return {"message": "Calendar Assistant API is running!", "status": "alive"}

@app.on_event("startup")
async def startup_event():
    """Start the keep-alive task when the app starts"""
    asyncio.create_task(keep_alive_ping())
    logger.info("Keep-alive service started")

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)