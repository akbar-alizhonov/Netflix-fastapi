import uvicorn
from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.config.logger import setup_logger
from src.config.middleware import setup_middlewares

app = FastAPI()
app.include_router(router_auth)
setup_middlewares(app)
setup_logger()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )