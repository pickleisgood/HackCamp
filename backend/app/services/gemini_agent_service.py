# Gemini AI Agent Service with Sequential Agents for restaurant discovery
import json
import re
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from app.config import settings
import requests

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class WebScraperAgent:
    """Agent dedicated to scraping and fetching restaurant information from the web"""
    
    def __init__(self):
        """Initialize web scraper agent"""
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_restaurants_web(self, location: str, filters: Dict) -> Dict:
        """
        Agent that searches for restaurants using web scraping and API calls.
        Converts filter criteria to a web search query.
        """
        print(f"🌐 Web Scraper Agent: Searching for restaurants in {location}")
        
        # Build search query from filters
        search_query = self._build_search_query(location, filters)
        
        try:
            # First, try to get results from Google Places-like query
            results = self._search_google_places_equivalent(location, filters)
            
            if results:
                print(f"✓ Web Scraper Agent: Found {len(results)} restaurants")
                return {
                    "raw_results": results,
                    "search_query": search_query,
                    "total_found": len(results),
                    "status": "success"
                }
            else:
                # Fallback: Use Gemini to generate realistic restaurant data based on location and filters
                return self._generate_restaurant_data(location, filters, search_query)
        
        except Exception as e:
            print(f"✗ Web Scraper Agent Error: {str(e)}")
            return {
                "raw_results": [],
                "error": str(e),
                "status": "error"
            }
    
    def _build_search_query(self, location: str, filters: Dict) -> str:
        """Convert filter criteria to a web search query"""
        query_parts = [location]
        
        if filters.get('cuisines'):
            query_parts.extend(filters['cuisines'])
        
        if filters.get('dietary'):
            query_parts.extend(filters['dietary'])
        
        if filters.get('budget'):
            query_parts.append(f"${len(filters['budget'][0])}")
        
        return " ".join(query_parts)
    
    def _search_google_places_equivalent(self, location: str, filters: Dict) -> List[Dict]:
        """
        Search for restaurants using web APIs and scraping.
        This could integrate with Google Places API or other restaurant databases.
        """
        # For now, use Gemini to search (simulating web search)
        prompt = f"""Find real restaurants in {location} matching these criteria:
        
Budget: {', '.join(filters.get('budget', ['$', '$$', '$$$', '$$$$']))}
Dietary: {', '.join(filters.get('dietary', ['Any']))}
Cuisine: {', '.join(filters.get('cuisines', ['Any']))}
Min Rating: {filters.get('minRating', 3.5)}

Return a JSON array of REAL, ACTUAL restaurants with exact names and addresses.
Format: [{{"name": "exact name", "address": "exact address", "cuisine": "type"}}]"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group())
                return results if isinstance(results, list) else []
        except Exception as e:
            print(f"Error in web search: {e}")
        
        return []
    
    def _generate_restaurant_data(self, location: str, filters: Dict, search_query: str) -> Dict:
        """Generate comprehensive restaurant data when web scraping unavailable"""
        print(f"📊 Web Scraper Agent: Generating restaurant data...")
        
        budget_map = {
            '$': 'Budget friendly (under $15 per person)',
            '$$': 'Moderate pricing ($15-$30 per person)',
            '$$$': 'Upscale ($30-$60 per person)',
            '$$$$': 'Fine dining ($60+ per person)'
        }
        
        budget_str = ', '.join([budget_map.get(b, b) for b in filters.get('budget', [])])
        dietary_str = ', '.join(filters.get('dietary', []))
        cuisines_str = ', '.join(filters.get('cuisines', []))
        min_rating = filters.get('minRating', 3.5)
        
        prompt = f"""Find 5-8 REAL, POPULAR restaurants in {location} with these exact criteria.
Only include restaurants that ACTUALLY EXIST and are well-known:

Location: {location}
Budget: {budget_str if budget_str else 'Any'}
Dietary Options: {dietary_str if dietary_str else 'Any'}
Cuisines: {cuisines_str if cuisines_str else 'Any'}
Minimum Rating: {min_rating}+

For each restaurant provide ACCURATE information:
- Exact restaurant name
- Real address
- Actual cuisine type
- Real phone number (if known)
- Website
- Approximate price range
- Real menu items
- Accessibility features

Return ONLY a valid JSON array:
[
  {{
    "name": "restaurant name",
    "address": "address",
    "phone": "phone",
    "website": "url",
    "cuisine": ["type1"],
    "rating": 4.5,
    "budget": "$$ or $$$",
    "hours": "Mon-Sun 11am-11pm",
    "wheelchair_accessible": true/false,
    "menu_items": ["dish1", "dish2", "dish3"],
    "service_types": ["Dine-in", "Takeout", "Delivery"]
  }}
]"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON array
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                raw_results = json.loads(json_match.group())
                return {
                    "raw_results": raw_results if isinstance(raw_results, list) else [],
                    "search_query": search_query,
                    "total_found": len(raw_results) if isinstance(raw_results, list) else 0,
                    "status": "success"
                }
        except Exception as e:
            print(f"Error generating data: {e}")
        
        return {
            "raw_results": [],
            "error": "Failed to generate restaurant data",
            "status": "error"
        }


class DataTransformerAgent:
    """Agent dedicated to transforming and formatting restaurant data for frontend display"""
    
    def __init__(self):
        """Initialize data transformer agent"""
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def transform_restaurant_data(self, raw_restaurants: List[Dict], filters: Dict) -> Dict:
        """
        Transform raw restaurant data into frontend-displayable format.
        Filters restaurants based on ALL criteria and enriches data.
        """
        print(f"🔄 Data Transformer Agent: Processing {len(raw_restaurants)} restaurants")
        
        restaurants_json = json.dumps(raw_restaurants, indent=2)
        filters_json = json.dumps(filters, indent=2)
        
        prompt = f"""You are a data transformer. Process these restaurants and filters.

RESTAURANTS:
{restaurants_json}

FILTERS (what user selected):
{filters_json}

TASK:
1. Filter restaurants that match ALL user criteria exactly
2. For each matching restaurant, add:
   - match_score (0-100 based on how well it matches ALL filters)
   - matching_menu_items (dishes that match dietary restrictions)
   - why_it_matches (explanation for user)
   - accessibility_features (list)
   - service_types_available (list)
3. Sort by match_score descending
4. Include coordinates as lat/lon (estimate if needed)

Return ONLY valid JSON:
{{
  "transformed_restaurants": [
    {{
      "id": "unique_id",
      "name": "restaurant name",
      "address": "full address",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "rating": 4.5,
      "budget": "$$ or $$$",
      "cuisines": ["type1", "type2"],
      "image": "url_if_available",
      "website": "url",
      "phone": "phone_number",
      "hours": "hours",
      "match_score": 95,
      "matching_menu_items": ["dish1", "dish2"],
      "why_it_matches": "reason",
      "accessibility_features": ["wheelchair"],
      "service_types": ["Dine-in", "Takeout"],
      "tags": ["tag1", "tag2"]
    }}
  ],
  "total_matching": 5,
  "search_summary": "Found 5 restaurants matching your criteria"
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                print(f"✓ Data Transformer Agent: Transformed {len(result.get('transformed_restaurants', []))} restaurants")
                return result
        except Exception as e:
            print(f"Error transforming data: {e}")
        
        return {
            "transformed_restaurants": [],
            "error": "Failed to transform restaurant data",
            "search_summary": "No results could be processed"
        }


class GeminiAgentService:
    """Main service orchestrating sequential agents for restaurant discovery"""
    
    def __init__(self):
        """Initialize all agents"""
        self.web_scraper = WebScraperAgent()
        self.data_transformer = DataTransformerAgent()
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def build_search_prompt(self, location: str, filters: Dict) -> str:
        """Build a detailed prompt for Gemini to search restaurants based on filters"""
        
        budget_map = {
            '$': 'Budget friendly (under $15 per person)',
            '$$': 'Moderate pricing ($15-$30 per person)',
            '$$$': 'Upscale ($30-$60 per person)',
            '$$$$': 'Fine dining ($60+ per person)'
        }
    
    def search_restaurants(self, location: str, filters: Dict) -> Dict:
        """
        Main orchestration method using sequential agents:
        1. WebScraperAgent: Finds real restaurants
        2. DataTransformerAgent: Transforms and filters data
        """
        print(f"\n{'='*60}")
        print(f"🔍 SEARCH INITIATED")
        print(f"Location: {location}")
        print(f"Filters: {filters}")
        print(f"{'='*60}\n")
        
        # STEP 1: Web Scraper Agent finds restaurants
        print("📍 STEP 1: Web Scraper Agent")
        print("-" * 60)
        web_search_result = self.web_scraper.search_restaurants_web(location, filters)
        
        if web_search_result.get("status") == "error" or not web_search_result.get("raw_results"):
            print(f"⚠️  No restaurants found by web scraper")
            return {
                "restaurants": [],
                "error": "No restaurants found matching your criteria",
                "searchSummary": "Search returned no results"
            }
        
        raw_restaurants = web_search_result.get("raw_results", [])
        print(f"✓ Found {len(raw_restaurants)} raw restaurant results\n")
        
        # STEP 2: Data Transformer Agent processes and filters
        print("📍 STEP 2: Data Transformer Agent")
        print("-" * 60)
        transformed_result = self.data_transformer.transform_restaurant_data(raw_restaurants, filters)
        
        if "error" in transformed_result:
            print(f"⚠️  Error during transformation: {transformed_result.get('error')}")
        
        final_restaurants = transformed_result.get("transformed_restaurants", [])
        print(f"✓ Transformed into {len(final_restaurants)} displayable restaurants\n")
        
        print(f"{'='*60}")
        print(f"✅ SEARCH COMPLETE")
        print(f"{'='*60}\n")
        
        return {
            "restaurants": final_restaurants,
            "totalFound": transformed_result.get("total_matching", len(final_restaurants)),
            "searchSummary": transformed_result.get("search_summary", f"Found {len(final_restaurants)} restaurants"),
            "filters_applied": filters
        }

