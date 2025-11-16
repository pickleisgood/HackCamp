from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.schemas import SearchRequest, SearchResponse, RestaurantResponse
from app.services.gemini_agent_service import GeminiAgentService
from app.utils.helpers import validate_filters
import os

router = APIRouter()

# Initialize services
gemini_service = GeminiAgentService()

@router.post("/search")
async def search_restaurants(request: SearchRequest) -> SearchResponse:
    """
    Search for restaurants based on location and filters using Gemini AI Agent
    
    Workflow:
    1. Validates location and filters
    2. Sends query to Gemini AI Agent
    3. AI Agent searches for restaurants matching all criteria
    4. Returns filtered results with restaurant details
    
    Args:
        request: SearchRequest containing location and optional filters
        
    Returns:
        SearchResponse with found restaurants and search metadata
    """
    try:
        # Validate location
        if not request.location or len(request.location.strip()) == 0:
            raise HTTPException(status_code=400, detail="Location is required")
        
        # Validate and prepare filters
        filters = validate_filters(request.filters.dict() if request.filters else {})
        
        print(f"🔍 Searching for restaurants in {request.location}")
        print(f"📋 Filters: {filters}")
        
        # Use Gemini AI Agent to search restaurants
        ai_response = gemini_service.search_restaurants(
            location=request.location,
            filters=filters
        )
        
        # Check for errors in AI response
        if "error" in ai_response and ai_response.get("restaurants") == []:
            print(f"⚠️ AI Error: {ai_response.get('error')}")
            raise HTTPException(
                status_code=500, 
                detail=f"AI search failed: {ai_response.get('error', 'Unknown error')}"
            )
        
        # Transform AI response to RestaurantResponse objects
        restaurants_data = []
        for restaurant in ai_response.get('restaurants', []):
            try:
                restaurant_obj = RestaurantResponse(
                    id=restaurant.get('id', restaurant.get('name', '').replace(' ', '_').lower()),
                    name=restaurant.get('name', 'Unknown'),
                    address=restaurant.get('address', ''),
                    latitude=float(restaurant.get('latitude', 0)),
                    longitude=float(restaurant.get('longitude', 0)),
                    rating=float(restaurant.get('rating', 0)),
                    budget=restaurant.get('budget', ''),
                    cuisines=restaurant.get('cuisines', []),
                    image=restaurant.get('image'),
                    website=restaurant.get('website'),
                    menuLink=restaurant.get('menuLink'),
                    matchingItems=restaurant.get('matching_menu_items', restaurant.get('matchingItems', [])),
                    phone=restaurant.get('phone', ''),
                    hours=restaurant.get('hours', ''),
                    accessibility=restaurant.get('accessibility_features', restaurant.get('accessibility', [])),
                    serviceTypes=restaurant.get('service_types', restaurant.get('serviceTypes', [])),
                    tags=restaurant.get('tags', []),
                    matchScore=restaurant.get('match_score'),
                    whyItMatches=restaurant.get('why_it_matches'),
                )
                restaurants_data.append(restaurant_obj)
            except Exception as e:
                print(f"⚠️ Error parsing restaurant data: {str(e)}")
                continue
        
        print(f"✅ Found {len(restaurants_data)} restaurants")
        
        return SearchResponse(
            totalFound=len(restaurants_data),
            restaurants=restaurants_data,
            location=request.location,
            filters=request.filters
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in search_restaurants: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/{restaurant_id}")
async def get_restaurant_details(restaurant_id: str) -> RestaurantResponse:
    """
    Get detailed information about a specific restaurant
    
    Args:
        restaurant_id: The ID of the restaurant
        
    Returns:
        RestaurantResponse with full restaurant details
    """
    try:
        # TODO: Implement restaurant details retrieval from cache or database
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_restaurants(
    location: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(10)
):
    """
    List restaurants with optional location filter
    
    Args:
        location: Optional location to filter by
        skip: Number of results to skip for pagination
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with restaurant list and pagination info
    """
    try:
        # TODO: Implement listing with pagination from database
        return {
            "total": 0,
            "restaurants": [],
            "skip": skip,
            "limit": limit
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

