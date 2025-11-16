# Restaurant Finder - HackCamp Project

## Overview
This is a full-stack web application for discovering restaurants based on user location, budget, dietary restrictions, ratings, and other preferences. The backend uses FastAPI with Gemini AI for intelligent filtering, and the frontend is built with React.

## Project Structure

```
HackCamp/
├── frontend/                    # React frontend application
│   ├── public/
│   │   └── index.html          # Main HTML entry point
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── SearchBar.jsx
│   │   │   ├── FilterOverlay.jsx
│   │   │   ├── MapContainer.jsx
│   │   │   ├── RestaurantList.jsx
│   │   │   └── RestaurantCard.jsx
│   │   ├── pages/              # Page components
│   │   │   └── LandingPage.jsx
│   │   ├── hooks/              # Custom React hooks (TBD)
│   │   ├── utils/              # Utility functions
│   │   │   └── api.js          # API client
│   │   ├── styles/             # CSS modules
│   │   │   ├── LandingPage.css
│   │   │   ├── SearchBar.css
│   │   │   ├── FilterOverlay.css
│   │   │   ├── MapContainer.css
│   │   │   ├── RestaurantList.css
│   │   │   └── RestaurantCard.css
│   │   ├── App.jsx             # Main app component
│   │   ├── App.css
│   │   ├── index.jsx           # React DOM render
│   │   └── index.css           # Global styles
│   ├── package.json            # Frontend dependencies
│   ├── .env.example            # Environment variables template
│   └── .gitignore
│
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── routes/             # API route handlers
│   │   │   ├── restaurants.py  # Restaurant search endpoints
│   │   │   └── health.py       # Health check endpoints
│   │   ├── services/           # Business logic services
│   │   │   ├── google_maps_service.py    # Google Maps integration
│   │   │   └── gemini_agent_service.py   # Gemini AI agent
│   │   ├── models/             # Data models
│   │   │   ├── schemas.py      # Pydantic schemas
│   │   │   └── restaurant.py   # Restaurant model
│   │   ├── utils/              # Utility functions
│   │   │   └── helpers.py      # Helper functions
│   │   ├── config.py           # Configuration and settings
│   │   └── __init__.py         # FastAPI app initialization
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Server entry point
│   ├── .env.example            # Environment variables template
│   └── .gitignore
│
├── Overview.txt                # Project requirements and features
└── README.md                   # This file
```

## Backend Features

- **FastAPI Framework**: Modern, fast Python web framework for building APIs
- **Gemini AI Integration**: Uses Google's Gemini 2.5 Flash model for intelligent restaurant filtering
- **Google Maps API**: Integration for location search, nearby restaurants, and ratings
- **CORS Support**: Cross-origin request handling for frontend communication
- **Input Validation**: Pydantic models for robust request/response validation

## Frontend Features

- **React 18**: Modern UI library with hooks
- **Responsive Design**: Mobile-first responsive layout
- **Google Maps Integration**: Interactive map display with restaurant pins
- **Infinite Scroll**: Efficient loading of large restaurant lists
- **Dynamic Filters**: Location, budget, dietary restrictions, ratings, and more
- **Professional UI**: Clean, user-friendly interface with gradient backgrounds

## Installation

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (copy from `.env.example` and fill in API keys):
   ```bash
   cp .env.example .env
   ```

5. Run the server:
   ```bash
   python run.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

4. Start development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints (Planned)

### Restaurants
- `POST /api/restaurants/search` - Search restaurants based on location and filters
- `GET /api/restaurants/{id}` - Get detailed information about a restaurant
- `GET /api/restaurants/` - List restaurants with optional filters

### Health
- `GET /health` - Health check
- `GET /version` - API version

## Environment Variables

### Frontend (.env)
```
REACT_APP_GOOGLE_MAPS_API_KEY=your_key_here
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Backend (.env)
```
GOOGLE_MAPS_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

## Filter Categories

1. **Budget**: $, $$, $$$, $$$$
2. **Dietary Restrictions**: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free, Halal, Kosher
3. **Cuisines**: Italian, Asian, Mexican, Indian, American, French
4. **Service Type**: Dine-In, Takeout, Delivery
5. **Accessibility**: Wheelchair Accessible, Accessible Washroom, Allergen Menu
6. **Operational Hours**: Open Now, Open Late, Breakfast, Lunch, Dinner
7. **Minimum Rating**: 3.5+, 4.0+, 4.5+

## Next Steps - Implementation Tasks

### Backend
- [ ] Implement Google Maps API integration
- [ ] Implement Gemini AI agent for restaurant filtering
- [ ] Set up database (SQLAlchemy ORM)
- [ ] Implement caching for frequently searched locations
- [ ] Add authentication/user profiles (optional)
- [ ] Add unit tests and integration tests
- [ ] Deploy to cloud platform

### Frontend
- [ ] Integrate Google Maps JavaScript API
- [ ] Connect all filters to backend search endpoint
- [ ] Implement infinite scroll pagination
- [ ] Add error handling and loading states
- [ ] Implement restaurant detail modal
- [ ] Add image carousel for restaurant photos
- [ ] Optimize performance and bundle size
- [ ] Add mobile responsiveness improvements
- [ ] Deploy to cloud platform

## Technologies Used

**Frontend:**
- React 18
- Axios (HTTP client)
- React Router (navigation)
- React Infinite Scroll Component
- Google Maps JavaScript API

**Backend:**
- FastAPI
- Pydantic (validation)
- Python 3.8+
- Google Maps API
- Google Generative AI (Gemini)

## Notes

- The Gemini API key is provided in the Overview.txt but should be moved to environment variables
- Theme is currently set to purple gradient (#667eea to #764ba2) - can be customized
- The app name and description should be finalized
- All TODO comments in code indicate areas needing implementation
- Database integration is not yet implemented - currently uses in-memory storage

## License

TBD

## Contact

For questions or issues, please refer to the project documentation or contact the development team.
