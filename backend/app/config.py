import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE = "Restaurant Finder API"
    API_VERSION = "0.1.0"
    API_DESCRIPTION = "Backend API for restaurant discovery application"
    
    # Google APIs
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Server Configuration
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Default values
    DEFAULT_SEARCH_RADIUS = 5000  # meters
    DEFAULT_MIN_RATING = 3.5
    MAX_RESULTS_PER_PAGE = 50
    
    # Database (placeholder)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
