from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import restaurants
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Restaurant Finder API",
    description="Backend API for restaurant discovery application",
    version="0.1.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants.router, prefix="/api/restaurants", tags=["restaurants"])

@app.get("/")
async def root():
    return {"message": "Restaurant Finder API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
