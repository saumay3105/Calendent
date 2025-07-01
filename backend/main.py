from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router


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

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
