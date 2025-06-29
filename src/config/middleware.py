from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI, middlewares: list | None = None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Request-Headers",
            "Set-Cookie",
            "Access-Control-Request-Origins"
        ],
    )

    if middlewares:
        for middleware in middlewares:
            app.add_middleware(middleware)
