from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import projects, sources, leads, milestones, ingest, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LUMO CRM API", version="1.0.0")

app.include_router(projects.router, prefix="/api/v1")
app.include_router(sources.router, prefix="/api/v1")
app.include_router(leads.router, prefix="/api/v1")
app.include_router(milestones.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")

@app.get("/")
def root():
    return{"message":"CRM is operational"}