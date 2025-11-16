# Gemini AI Agent Service for restaurant filtering
import json
from typing import List, Dict, Optional
import google.generativeai as genai
from app.config import settings

class GeminiAgentService:
    """Service for Gemini AI agent interactions for restaurant discovery and filtering"""
    
    def __init__(self):
        """Initialize Gemini client with API key"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def build_search_prompt(self, location: str, filters: Dict) -> str:
        """Build a detailed prompt for Gemini to search restaurants based on filters"""
        
        budget_map = {
            '$': 'Budget friendly (under $15 per person)',
            '$$': 'Moderate pricing ($15-$30 per person)',
            '$$$': 'Upscale ($30-$60 per person)',
            '$$$$': 'Fine dining ($60+ per person)'
        }
        
        budget_str = ', '.join([budget_map.get(b, b) for b in filters.get('budget', [])])
        dietary_str = ', '.join(filters.get('dietary', []))
        cuisines_str = ', '.join(filters.get('cuisines', []))
        service_str = ', '.join(filters.get('serviceType', []))
        accessibility_str = ', '.join(filters.get('accessibility', []))
        operational_str = ', '.join(filters.get('operational', []))
        min_rating = filters.get('minRating', 3.5)
        
        prompt = f"""You are a restaurant discovery AI agent. Find the BEST restaurants in {location} that match these specific criteria:

**Search Criteria:**
- Location: {location}
- Budget Level: {budget_str if budget_str else 'Any budget'}
- Dietary Restrictions/Preferences: {dietary_str if dietary_str else 'No specific restrictions'}
- Cuisine Types: {cuisines_str if cuisines_str else 'Any cuisine'}
- Service Types Needed: {service_str if service_str else 'Any service type'}
- Accessibility Features: {accessibility_str if accessibility_str else 'No specific requirements'}
- When to Dine: {operational_str if operational_str else 'Anytime'}
- Minimum Rating: {min_rating}+ stars

**Task:**
1. Research and find 3-5 high-quality restaurants that match ALL of these criteria
2. For each restaurant, provide:
   - Name (EXACT restaurant name)
   - Address and location
   - Estimated price range ($, $$, $$$, or $$$$)
   - Cuisine type
   - Google Maps rating (estimate if not exact)
   - 2-3 menu items that match the dietary restrictions
   - Service types available (Dine-in, Takeout, Delivery)
   - Website URL (if known)
   - Accessibility features
   - Operating hours summary

3. IMPORTANT: Focus on accuracy and real restaurants. If unsure, indicate confidence level.

**Return format:**
Return ONLY valid JSON (no markdown, no code blocks) in this exact format:
{{
  "restaurants": [
    {{
      "name": "Restaurant Name",
      "address": "Street Address, City, State, ZIP",
      "budget": "$$ or $$$, etc",
      "cuisines": ["Cuisine1", "Cuisine2"],
      "rating": 4.5,
      "matchingItems": ["Dish 1 matching dietary", "Dish 2 matching dietary"],
      "serviceTypes": ["Dine-In", "Takeout"],
      "website": "https://website.com",
      "accessibility": ["Wheelchair Accessible"],
      "hours": "Mon-Sun 11am-11pm (or similar)",
      "matchNotes": "Why this restaurant matches the criteria"
    }}
  ],
  "searchSummary": "Brief summary of what was found",
  "confidence": "high/medium/low"
}}

Now search and return results for {location}:"""
        
        return prompt
    
    def search_restaurants(self, location: str, filters: Dict) -> Dict:
        """Use Gemini AI to search for restaurants matching user criteria"""
        try:
            prompt = self.build_search_prompt(location, filters)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse JSON response - try to extract JSON from response
            try:
                # Try direct JSON parsing first
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from the response (in case there's extra text)
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    # Return structured error response
                    return {
                        "restaurants": [],
                        "error": "Could not parse AI response",
                        "rawResponse": response_text[:200]
                    }
            
            return result
            
        except Exception as e:
            print(f"Error in Gemini search: {str(e)}")
            return {
                "restaurants": [],
                "error": f"AI search error: {str(e)}"
            }
    
    def filter_restaurants_by_dietary(self, restaurants: List[Dict], dietary_restrictions: List[str]) -> List[Dict]:
        """Filter restaurants based on dietary restrictions"""
        if not dietary_restrictions:
            return restaurants
        
        prompt = f"""Given these restaurants and dietary restrictions, identify which restaurants are best matches:

Dietary Restrictions: {', '.join(dietary_restrictions)}

Restaurants:
{json.dumps(restaurants, indent=2)}

Return a JSON object with:
- "filtered_restaurants": list of restaurant indices that match
- "recommendations": brief explanation for each match

Return ONLY valid JSON:"""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            print(f"Error filtering by dietary: {str(e)}")
            return {"filtered_restaurants": [], "error": str(e)}
    
    def find_matching_menu_items(self, restaurant: Dict, dietary_restrictions: List[str]) -> List[str]:
        """Use Gemini to identify menu items matching dietary restrictions"""
        if not dietary_restrictions or not restaurant.get('matchingItems'):
            return restaurant.get('matchingItems', [])
        
        prompt = f"""Given this restaurant and dietary restrictions, suggest the best menu items:

Restaurant: {restaurant.get('name', 'Unknown')}
Cuisine: {', '.join(restaurant.get('cuisines', []))}
Dietary Restrictions: {', '.join(dietary_restrictions)}
Current Menu Items: {json.dumps(restaurant.get('matchingItems', []))}

Suggest 3-4 realistic menu items from {restaurant.get('name')} that satisfy these restrictions.
Return ONLY a JSON array of strings with menu items:"""
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON array from response
            response_text = response.text.strip()
            result = json.loads(response_text)
            if isinstance(result, list):
                return result
            return restaurant.get('matchingItems', [])
        except Exception as e:
            print(f"Error finding menu items: {str(e)}")
            return restaurant.get('matchingItems', [])
    
    def rank_restaurants(self, restaurants: List[Dict], user_preferences: Dict) -> List[Dict]:
        """Use Gemini to rank restaurants based on how well they match user preferences"""
        if not restaurants:
            return restaurants
        
        preferences_str = json.dumps(user_preferences, indent=2)
        restaurants_str = json.dumps(restaurants, indent=2)
        
        prompt = f"""Rank these restaurants based on how well they match the user's preferences:

User Preferences:
{preferences_str}

Restaurants:
{restaurants_str}

Return ONLY a JSON object:
{{
  "ranked_restaurants": [ordered list of restaurants by relevance],
  "ranking_notes": {{restaurant_name: "reason for this ranking", ...}}
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            # Clean up if needed
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get('ranked_restaurants', restaurants)
            return restaurants
        except Exception as e:
            print(f"Error ranking restaurants: {str(e)}")
            return restaurants
    
    def enhance_restaurant_data(self, restaurants: List[Dict]) -> List[Dict]:
        """Use Gemini to enhance restaurant data with additional information"""
        if not restaurants:
            return restaurants
        
        prompt = f"""Enhance these restaurant entries with additional helpful information:

{json.dumps(restaurants, indent=2)}

For each restaurant, add if missing:
- Why customers love this restaurant (2-3 sentences)
- Best time to visit
- Popular dishes
- Ambiance description

Return ONLY valid JSON with enhanced restaurant data:"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            result = json.loads(response_text)
            if isinstance(result, dict) and 'restaurants' in result:
                return result['restaurants']
            elif isinstance(result, list):
                return result
            return restaurants
        except Exception as e:
            print(f"Error enhancing data: {str(e)}")
            return restaurants

