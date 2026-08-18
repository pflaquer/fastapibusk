import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

# Import your database elements
from .database import get_db, engine, Base

# This function runs automatically the second Render starts your server
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safely connect to Postgres and create database tables if they are missing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Initialize the FastAPI app with the lifespan table generator
app = FastAPI(title="My Scalable App", lifespan=lifespan)

# Get the absolute path to the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files and initialize Jinja2 templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Main Home Page Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Modern explicit syntax prevents the Jinja2 tuple/dict dictionary error
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={"title": "Home"}
    )

# HTMX Partial Snippet Route
@app.post("/clicked", response_class=HTMLResponse)
async def clicked_handler(db: AsyncSession = Depends(get_db)):
    # Your async database code can be processed here safely using 'db'
    # e.g., result = await db.execute(select(MyModel))
    
    # Return a lightweight fragment. HTMX swaps this directly into the DOM
    return "<span>⚡ Dynamic server-side content loaded asynchronously!</span>"
