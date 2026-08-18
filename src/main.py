import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
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

# Get the absolute directory where main.py actually lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Self-healing templates directory creator
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Initialize Jinja2 templates safely
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Main Home Page Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse(
            request=request, 
            name="home.html", 
            context={"title": "Home"}
        )
    except Exception:
        # Emergency fallback layout so your app loads even if home.html isn't pushed to Git yet!
        fallback_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Scalable App</title>
            <script src="https://unpkg.com"></script>
            <style>body { font-family: sans-serif; background: #f4f4f9; padding: 40px; text-align: center; }</style>
        </head>
        <body>
            <h1>⚡ FastAPI + HTMX Monolith is Live!</h1>
            <p>Your asynchronous Python backend is successfully running on Render.</p>
            <button hx-post="/clicked" hx-target="#msg" hx-swap="innerHTML" style="padding:10px 20px; background:#0070f3; color:white; border:none; border-radius:5px; cursor:pointer;">
                Test Async Event Loop
            </button>
            <div id="msg" style="margin-top:20px; font-weight:bold; color:green;"></div>
        </body>
        </html>
        """
        return HTMLResponse(content=fallback_html)

# HTMX Partial Snippet Route
@app.post("/clicked", response_class=HTMLResponse)
async def clicked_handler(db: AsyncSession = Depends(get_db)):
    return "<span>⚡ Dynamic server-side content loaded via async event loop!</span>"
