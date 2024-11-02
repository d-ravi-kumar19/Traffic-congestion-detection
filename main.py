from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
from app.middleware.route_not_found_middleware import RouteNotFoundMiddleware 
import logging
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app.logger = logger 

# Setup CORS for API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory=os.path.join("app", "static")), name="static")

# Include API router
app.include_router(api_router, prefix="/api/v1", tags=["api"])

@app.get("/config")
async def get_config():
    return {"api_url": os.getenv("API_URL")}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle not found routes with custom middleware
app.add_middleware(RouteNotFoundMiddleware)

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
