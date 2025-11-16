"""
Test script for the sequential Gemini agents
Run this to verify the agents work correctly
"""

import json
import sys
sys.path.insert(0, '/Users/andrexue/GitHub/HackCamp/backend')

from app.services.gemini_agent_service import GeminiAgentService

def test_search():
    """Test the sequential agent search"""
    
    service = GeminiAgentService()
    
    # Example search
    location = "San Francisco, CA"
    filters = {
        "budget": ["$$", "$$$"],
        "dietary": ["Vegetarian"],
        "cuisines": ["Italian", "Mediterranean"],
        "minRating": 4.0,
        "serviceType": ["Dine-in", "Takeout"],
        "accessibility": ["Wheelchair Accessible"],
        "operational": []
    }
    
    print("\n" + "="*70)
    print("🚀 TESTING SEQUENTIAL AGENTS")
    print("="*70)
    print(f"\nSearching for restaurants in: {location}")
    print(f"Filters: {json.dumps(filters, indent=2)}")
    
    result = service.search_restaurants(location, filters)
    
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"\nTotal Found: {result.get('totalFound', 0)}")
    print(f"Search Summary: {result.get('searchSummary', 'N/A')}")
    
    restaurants = result.get('restaurants', [])
    if restaurants:
        print(f"\n✅ Found {len(restaurants)} restaurants:\n")
        for i, rest in enumerate(restaurants, 1):
            print(f"{i}. {rest.get('name', 'Unknown')}")
            print(f"   Address: {rest.get('address', 'N/A')}")
            print(f"   Rating: {rest.get('rating', 'N/A')} stars")
            print(f"   Budget: {rest.get('budget', 'N/A')}")
            print(f"   Match Score: {rest.get('match_score', 'N/A')}/100")
            print(f"   Why It Matches: {rest.get('why_it_matches', 'N/A')}")
            print(f"   Menu Items: {', '.join(rest.get('matching_menu_items', []))}")
            print()
    else:
        print(f"\n⚠️  No restaurants found")
        if result.get('error'):
            print(f"Error: {result.get('error')}")
    
    print("="*70)

if __name__ == "__main__":
    test_search()
