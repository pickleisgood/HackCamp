# Development and setup guide for the Restaurant Finder project

## Quick Start Guide

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)
- npm or yarn (for frontend package management)

### Step-by-Step Setup

#### Backend Setup
```bash
# 1. Navigate to backend directory
cd backend

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your API keys
cp .env.example .env
# Edit .env and add:
# - GOOGLE_MAPS_API_KEY
# - GEMINI_API_KEY

# 6. Run the server
python run.py
# Backend will run on http://localhost:8000
```

#### Frontend Setup
```bash
# 1. Navigate to frontend directory (from root)
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
cp .env.example .env
# Edit .env and add:
# - REACT_APP_GOOGLE_MAPS_API_KEY
# - REACT_APP_BACKEND_URL=http://localhost:8000

# 4. Start development server
npm start
# Frontend will run on http://localhost:3000
```

### Verification

- Frontend: Navigate to `http://localhost:3000`
- Backend API: Visit `http://localhost:8000/docs` (Swagger UI)
- Backend Health: `http://localhost:8000/health`

## Project Overview

### Frontend Architecture
- **Components**: Reusable UI components with React hooks
- **Pages**: Full page components (currently LandingPage)
- **Utils**: API client and helper functions
- **Styles**: CSS files for each component for better organization

### Backend Architecture
- **Routes**: API endpoint handlers organized by resource
- **Services**: Business logic (Google Maps, Gemini AI integration)
- **Models**: Data validation schemas (Pydantic)
- **Utils**: Helper functions for common operations

## Key Features to Implement

### High Priority
1. Google Maps API Integration
   - Geocoding user input location
   - Displaying restaurants on map
   - Real-time rating display

2. Gemini AI Agent
   - Parse restaurant data from web
   - Match menu items to dietary restrictions
   - Intelligent filtering based on preferences

3. Frontend-Backend Communication
   - Connect search form to API
   - Handle filter selections
   - Display results with pagination

### Medium Priority
4. Advanced Filters
   - Accessibility options
   - Operational hours
   - Social vibe matching

5. Restaurant Details
   - Photo carousel
   - Full menu display
   - Review aggregation

### Lower Priority
6. User Features
   - Save favorite restaurants
   - Search history
   - Custom preferences

## API Design

### Search Endpoint
```
POST /api/restaurants/search
Content-Type: application/json

{
  "location": "San Francisco, CA",
  "filters": {
    "budget": ["$", "$$"],
    "dietary": ["Vegetarian"],
    "cuisines": ["Italian", "Asian"],
    "minRating": 4.0,
    "serviceType": ["Dine-In", "Takeout"],
    "accessibility": ["Wheelchair Accessible"],
    "operational": ["Open Now"]
  },
  "radius": 5000
}

Response:
{
  "totalFound": 42,
  "location": "San Francisco, CA",
  "restaurants": [
    {
      "id": "...",
      "name": "Restaurant Name",
      "address": "123 Main St",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "rating": 4.5,
      "budget": "$$",
      "cuisines": ["Italian"],
      "image": "url...",
      "website": "url...",
      "menuLink": "url...",
      "matchingItems": ["Pasta Primavera", "Veggie Risotto"],
      "phone": "+1-555-0123",
      "hours": {...},
      "serviceTypes": ["Dine-In", "Takeout"],
      "accessibility": ["Wheelchair Accessible"]
    }
  ]
}
```

## Important Notes

- **API Keys**: Never commit API keys. Use .env files
- **CORS**: Backend is configured to allow frontend requests
- **Database**: Currently uses in-memory storage, integrate proper database for production
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Error Handling**: Add comprehensive error handling throughout
- **Testing**: Add unit and integration tests before deployment

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify all dependencies installed: `pip list`
- Check .env file is properly configured

### Frontend won't start
- Check if port 3000 is available
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check .env file in frontend directory

### API calls failing
- Verify backend is running on http://localhost:8000
- Check CORS settings in backend/app/__init__.py
- Verify .env variables are set correctly
- Check browser console for specific error messages

## Next Team Member Onboarding

1. Read this SETUP.md file
2. Follow the Step-by-Step Setup section
3. Review the Project Architecture section
4. Check the README.md for additional context
5. Look for TODO comments in code - these indicate implementation areas
6. Start with high-priority features

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Google Maps API Documentation](https://developers.google.com/maps)
- [Google Generative AI Documentation](https://ai.google.dev/)

---

Last Updated: November 15, 2025
