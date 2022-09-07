import logging
from typing import Any
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.titanic import titanic_router

app = FastAPI()
root_router = APIRouter()
logging.basicConfig(level=logging.INFO)


@root_router.get("/")
def index() -> Any:
    body = """
        <html>
            <body style='padding: 20px;'>
                <h1>ML playground api</h1>
                <div>
                    Check the docs: <a href='/docs'>api docs</a>
                </div>
            </body>
        </html>
        """
    return HTMLResponse(content=body)


app.include_router(titanic_router)
app.include_router(root_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
