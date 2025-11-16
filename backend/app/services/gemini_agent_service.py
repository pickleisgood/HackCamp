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
- Real menu items matching dietary needs
- Accessibility features
- Latitude and Longitude coordinates
- Image URL (use unsplash.com food images or real restaurant photos if available)

Return ONLY a valid JSON array with no markdown:
[
  {{
    "name": "restaurant name",
    "address": "full address with street, city, state, zip",
    "phone": "phone number",
    "website": "https://website.com",
    "cuisine": ["type1", "type2"],
    "rating": 4.5,
    "budget": "$$ or $$$",
    "hours": "Mon-Sun 11am-11pm",
    "wheelchair_accessible": true,
    "image": "https://image-url.com/photo.jpg",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "menu_items": ["dish1 - description", "dish2 - description"],
    "service_types": ["Dine-in", "Takeout", "Delivery"]
  }}
]"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            # Extract JSON array
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                raw_results = json.loads(json_match.group())
                # Ensure all results have required fields
                for result in raw_results:
                    if 'latitude' not in result or not result['latitude']:
                        result['latitude'] = self._geocode_address(result.get('address', location))['lat']
                    if 'longitude' not in result or not result['longitude']:
                        result['longitude'] = self._geocode_address(result.get('address', location))['lng']
                    if 'image' not in result or not result['image']:
                        result['image'] = f"https://via.placeholder.com/400x300?text={result.get('name', 'Restaurant')}"
                
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
    
    def _geocode_address(self, address: str) -> Dict:
        """Simple geocoding - returns approximate coordinates"""
        # This is a fallback - in production you'd use Google Geocoding API
        # For now, return approximate coordinates for major cities
        location_coords = {
            'new york': {'lat': 40.7128, 'lng': -74.0060},
            'los angeles': {'lat': 34.0522, 'lng': -118.2437},
            'chicago': {'lat': 41.8781, 'lng': -87.6298},
            'san francisco': {'lat': 37.7749, 'lng': -122.4194},
            'seattle': {'lat': 47.6062, 'lng': -122.3321},
            'boston': {'lat': 42.3601, 'lng': -71.0589},
            'miami': {'lat': 25.7617, 'lng': -80.1918},
        }
        
        address_lower = address.lower()
        for city, coords in location_coords.items():
            if city in address_lower:
                return coords
        
        # Default to NYC if not found
        return {'lat': 40.7128, 'lng': -74.0060}


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
        
        # Build dietary requirements summary
        dietary_requirements = filters.get('dietary', [])
        dietary_str = ', '.join(dietary_requirements) if dietary_requirements else 'None specified'
        
        prompt = f"""You are a data transformer. Process these restaurants and filters.

RESTAURANTS:
{restaurants_json}

FILTERS (what user selected):
{filters_json}

DIETARY REQUIREMENTS: {dietary_str}

TASK:
1. Filter restaurants that match ALL user criteria exactly
2. For each matching restaurant, add:
   - match_score (0-100 based on how well it matches ALL filters, especially dietary)
   - matching_menu_items (dishes that match dietary restrictions - ONLY include items that fit their dietary needs)
   - why_it_matches (explanation for user emphasizing dietary accommodation)
   - accessibility_features (list)
   - service_types_available (list)
3. Sort by match_score descending
4. Include coordinates as lat/lon (estimate if needed)
5. IMPORTANT: Only include restaurants that can accommodate the dietary restrictions

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
      "tags": ["tag1", "tag2"],
      "dietary_accommodation": "description of how they accommodate dietary needs"
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


class DietaryValidationAgent:
    """Agent dedicated to validating that restaurants truly accommodate dietary restrictions"""
    
    def __init__(self):
        """Initialize dietary validation agent"""
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def validate_dietary_match(self, restaurants: List[Dict], dietary_requirements: List[str]) -> Dict:
        """
        Validate that restaurants genuinely accommodate dietary restrictions.
        Removes restaurants that don't truly align with dietary needs.
        """
        if not dietary_requirements:
            print("✓ Dietary Validation Agent: No dietary restrictions - skipping validation")
            return {
                "validated_restaurants": restaurants,
                "total_validated": len(restaurants),
                "removed_count": 0
            }
        
        print(f"🥗 Dietary Validation Agent: Validating {len(restaurants)} restaurants against dietary requirements")
        
        restaurants_json = json.dumps(restaurants, indent=2)
        dietary_str = ', '.join(dietary_requirements)
        
        prompt = f"""You are a dietary validation expert. Evaluate if these restaurants truly support these dietary needs.

RESTAURANTS:
{restaurants_json}

DIETARY REQUIREMENTS TO VALIDATE: {dietary_str}

TASK:
1. For each restaurant, verify it ACTUALLY supports the dietary requirements
2. Check their menu items and offerings align with the restrictions
3. Remove restaurants that don't genuinely accommodate these dietary needs
4. Keep only restaurants that have substantial menu options for these dietary requirements
5. For kept restaurants, add "dietary_match_confidence" (0-100) indicating how well they accommodate

RULES FOR EACH DIETARY REQUIREMENT:
- Vegetarian: Must have substantial vegetable-based dishes, no meat
- Vegan: Must have plant-based dishes with no animal products
- Gluten-Free: Must offer gluten-free alternatives or naturally gluten-free dishes
- Dairy-Free: Must have dishes without dairy products
- Nut-Free: Must be able to prepare dishes without nuts
- Halal: Must follow halal food preparation standards
- Kosher: Must follow kosher food preparation standards

Return ONLY valid JSON:
{{
  "validated_restaurants": [
    {{
      ...all restaurant fields,
      "dietary_match_confidence": 95,
      "dietary_validation_notes": "reason why this restaurant matches the dietary requirements"
    }}
  ],
  "total_validated": 5,
  "removed_count": 2,
  "removal_reasons": ["Restaurant X didn't have enough vegetarian options", "Restaurant Y not certified"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                removed = result.get('removed_count', 0)
                validated = len(result.get('validated_restaurants', []))
                print(f"✓ Dietary Validation Agent: {validated} restaurants passed validation, {removed} removed")
                return result
        except Exception as e:
            print(f"Error validating dietary match: {e}")
        
        return {
            "validated_restaurants": restaurants,
            "total_validated": len(restaurants),
            "removed_count": 0
        }


class GeminiAgentService:
    """Main service orchestrating sequential agents for restaurant discovery"""
    
    def __init__(self):
        """Initialize all agents"""
        self.web_scraper = WebScraperAgent()
        self.data_transformer = DataTransformerAgent()
        self.dietary_validator = DietaryValidationAgent()
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
        1. WebScraperAgent: Finds real restaurants with dietary considerations
        2. DataTransformerAgent: Transforms and filters data
        3. DietaryValidationAgent: Validates dietary accommodation
        """
        print(f"\n{'='*60}")
        print(f"🔍 SEARCH INITIATED")
        print(f"Location: {location}")
        print(f"Filters: {filters}")
        print(f"{'='*60}\n")
        
        # STEP 1: Web Scraper Agent finds restaurants (now with dietary awareness)
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
        
        transformed_restaurants = transformed_result.get("transformed_restaurants", [])
        print(f"✓ Transformed into {len(transformed_restaurants)} displayable restaurants\n")
        
        # STEP 3: Dietary Validation Agent validates dietary restrictions
        print("📍 STEP 3: Dietary Validation Agent")
        print("-" * 60)
        dietary_requirements = filters.get('dietary', [])
        if dietary_requirements:
            validation_result = self.dietary_validator.validate_dietary_match(
                transformed_restaurants, 
                dietary_requirements
            )
            final_restaurants = validation_result.get("validated_restaurants", [])
            print(f"✓ Validated {len(final_restaurants)} restaurants for dietary requirements\n")
        else:
            final_restaurants = transformed_restaurants
            print(f"✓ No dietary restrictions to validate\n")
        
        print(f"{'='*60}")
        print(f"✅ SEARCH COMPLETE")
        print(f"{'='*60}\n")
        
        return {
            "restaurants": final_restaurants,
            "totalFound": len(final_restaurants),
            "searchSummary": f"Found {len(final_restaurants)} restaurants matching your criteria",
            "filters_applied": filters
        }

