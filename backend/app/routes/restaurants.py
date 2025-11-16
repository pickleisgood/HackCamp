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
                # Only use REAL restaurant images - no generic fallbacks or example URLs
                restaurant_image = restaurant.get('image')
                restaurant_name = restaurant.get('name', 'Unknown')
                restaurant_website = restaurant.get('website')
                
                # Validate that image is a real restaurant image (not generic placeholder or example URL)
                if restaurant_image:
                    # Reject generic placeholder services and example.com URLs
                    if any(generic in restaurant_image.lower() for generic in ['picsum', 'unsplash', 'placeholder', 'via.placeholder', 'example.com', 'example.org', 'lorem', 'dummy']):
                        print(f"⚠️ Rejected invalid/placeholder URL for {restaurant_name}: {restaurant_image}")
                        restaurant_image = None
                    elif not restaurant_image.startswith('http'):
                        print(f"⚠️ Invalid image URL for {restaurant_name}: {restaurant_image}")
                        restaurant_image = None
                
                # If no valid image, try to fetch a real one
                if not restaurant_image:
                    print(f"📸 Attempting to fetch real restaurant image for {restaurant_name}...")
                    from app.services.google_maps_service import GoogleMapsService
                    google_maps = GoogleMapsService()
                    
                    # Try website first
                    if restaurant_website:
                        try:
                            real_image = google_maps.get_image_from_website(restaurant_website, restaurant_name)
                            if real_image:
                                restaurant_image = real_image
                                print(f"✓ Found real image from website for {restaurant_name}")
                        except Exception as e:
                            print(f"  ✗ Website scraping failed: {e}")
                    
                    # Try Google Maps if website didn't work
                    if not restaurant_image:
                        try:
                            location = request.location
                            real_image = google_maps.get_restaurant_photo(restaurant_name, location)
                            if real_image:
                                restaurant_image = real_image
                                print(f"✓ Found real image from Google Maps for {restaurant_name}")
                        except Exception as e:
                            print(f"  ✗ Google Maps failed: {e}")
                
                if not restaurant_image:
                    print(f"❌ No real restaurant image available for {restaurant_name} - will show placeholder in UI")
                    restaurant_image = None
                
                restaurant_obj = RestaurantResponse(
                    id=restaurant.get('id', restaurant.get('name', '').replace(' ', '_').lower()),
                    name=restaurant_name,
                    address=restaurant.get('address', ''),
                    latitude=float(restaurant.get('latitude', 0)),
                    longitude=float(restaurant.get('longitude', 0)),
                    rating=float(restaurant.get('rating', 0)),
                    budget=restaurant.get('budget', ''),
                    cuisines=restaurant.get('cuisines', []),
                    image=restaurant_image,
                    website=restaurant.get('website') or restaurant.get('website_url'),
                    menuLink=restaurant.get('menuLink') or restaurant.get('menu_url'),
                    matchingItems=restaurant.get('matching_menu_items', restaurant.get('matchingItems', [])),
                    phone=restaurant.get('phone', ''),
                    hours=restaurant.get('hours', ''),
                    accessibility=restaurant.get('accessibility_features', restaurant.get('accessibility', [])),
                    serviceTypes=restaurant.get('service_types', restaurant.get('serviceTypes', [])),
                    tags=restaurant.get('tags', []),
                    matchScore=restaurant.get('match_score'),
                    whyItMatches=restaurant.get('why_it_matches'),
                )
                print(f"✅ Restaurant {restaurant_name}")
                restaurants_data.append(restaurant_obj)
            except Exception as e:
                print(f"⚠️ Error parsing restaurant data: {str(e)}")
                import traceback
                traceback.print_exc()
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

