# 🍽️ Restaurant Finder

<img src="Images/logo.png" alt="Restaurant Finder Logo" width="200"/>

A smart restaurant discovery platform that uses AI to find the perfect restaurant based on your preferences.

## What It Does

Search for restaurants by location, budget, cuisine, dietary restrictions, and ratings. Our AI assistant learns your preferences and recommends the best matches.

**Tech Stack:**
- **Frontend**: React 18 with interactive maps
- **Backend**: FastAPI with Google's Gemini AI
- **APIs**: Google Maps for location & restaurant data

## Quick Start

Run everything with one command:

```bash
./run.sh <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
```

This will automatically:
- Set up backend virtual environment and dependencies
- Start the FastAPI backend at `http://localhost:8000`
- Install frontend dependencies
- Start the React frontend at `http://localhost:3000`

## Features

### Search Filters
- Budget ($, $$, $$$, $$$$)
- Dietary restrictions (Vegetarian, Vegan, Gluten-Free, etc.)
- Cuisines (Italian, Asian, Mexican, Indian, etc.)
- Service type (Dine-In, Takeout, Delivery)
- Accessibility options
- Rating thresholds (3.5+, 4.0+, 4.5+)
