import sys
from os import path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

BASH = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(0, BASH)

from tools_main.routers import init_routes


def init_app():
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routes(fastapi_app)

    return fastapi_app


if __name__ == '__main__':
    app = init_app()
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
