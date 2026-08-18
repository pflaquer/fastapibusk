import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})

# This endpoint handles the HTMX call and returns a raw HTML fragment
@app.post("/clicked", response_class=HTMLResponse)
async def clicked_handler(db: AsyncSession = Depends(get_db)):
    # You can perform lightning-fast async database actions here:
    # result = await db.execute(select(User))
    
    # We return a tiny piece of HTML. HTMX stitches it directly into the page!
    return "<span>⚡ Dynamic server-side content loaded asynchronously!</span>"
