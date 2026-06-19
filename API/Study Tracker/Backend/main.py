from fastapi import FastAPI
from routers.sessions import router as session_router

app = FastAPI()
app.include_router(session_router)