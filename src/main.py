import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="My Scalable App")

# Get absolute path to the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files and initialize Jinja2 templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This renders home.html and passes the required request context
    return templates.TemplateResponse("home.html", {"request": request, "title": "Welcome"})
