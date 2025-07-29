
from fastapi import FastAPI, Response

from app.routers.videocall import router as videocall_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(videocall_router)


@app.get("/")
def root():
    return Response("Server is running!", media_type="text/plain")

