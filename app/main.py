from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from . import models 
from .database import engine 
from .routers import posts, users, auth,  vote
from .config import settings

#only need the command below if not using alembic
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

#home page
@app.get("/" , response_class=HTMLResponse)
def root():
    return """
        <body>
            <h1>-- Hello World -- اسلام علیکم -- </h1>
        </body>
        """
