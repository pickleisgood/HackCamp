# 🍽️ Restaurant Finder

A smart restaurant discovery platform that uses AI to find the perfect restaurant based on your preferences.

## What It Does

Search for restaurants by location, budget, cuisine, dietary restrictions, and ratings. Our AI assistant learns your preferences and recommends the best matches.

**Tech Stack:**
- **Frontend**: React 18 with interactive maps
- **Backend**: FastAPI with Google's Gemini AI
- **APIs**: Google Maps for location & restaurant data

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py <GOOGLE_MAPS_API_KEY> <GEMINI_API_KEY>
```
Backend runs at `http://localhost:8000`

Example:
```bash
python3 run.py AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks AIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
```

### Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs at `http://localhost:3000`

## Features

### Search Filters
- Budget ($, $$, $$$, $$$$)
- Dietary restrictions (Vegetarian, Vegan, Gluten-Free, etc.)
- Cuisines (Italian, Asian, Mexican, Indian, etc.)
- Service type (Dine-In, Takeout, Delivery)
- Accessibility options
- Rating thresholds (3.5+, 4.0+, 4.5+)
