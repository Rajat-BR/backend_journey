from fastapi import FastAPI
from routers.books import router

app = FastAPI()
app.include_router(router)