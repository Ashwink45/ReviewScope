from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import run_pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve assets folder
app.mount(
    "/assets",
    StaticFiles(directory="frontend/plain-free-bootstrap-admin-template-main/assets"),
    name="assets"
)

# Serve frontend homepage
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/plain-free-bootstrap-admin-template-main/index.html")

class AppRequest(BaseModel):
    app_id: str

@app.post("/analyze")
def analyze(data: AppRequest):
    return run_pipeline(data.app_id)