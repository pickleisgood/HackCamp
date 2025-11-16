# Google Maps integration for restaurant search, geocoding, and photo retrieval
import googlemaps
from typing import Optional, Dict, List
from app.config import settings

class GoogleMapsService:
    """Service for Google Maps API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GOOGLE_MAPS_API_KEY
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None
            print("⚠️ Google Maps API key not configured - photo fetching will be limited")
    
    def geocode_location(self, location: str) -> Dict:
        """Convert location string to coordinates"""
        if not self.client:
            return {'lat': 0, 'lng': 0}
        
        try:
            geocode_result = self.client.geocode(location)
            if geocode_result:
                location_data = geocode_result[0]['geometry']['location']
                return {'lat': location_data['lat'], 'lng': location_data['lng']}
        except Exception as e:
            print(f"Error geocoding location: {e}")
        
        return {'lat': 0, 'lng': 0}
    
    def search_place_by_name(self, name: str, location: str) -> Optional[Dict]:
        """Search for a place by name and location"""
        if not self.client:
            return None
        
        try:
            # Search for the place using text search
            places_result = self.client.places(
                query=f"{name} restaurant {location}",
                type='restaurant'
            )
            
            if places_result and places_result.get('results'):
                place = places_result['results'][0]
                return {
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'rating': place.get('rating'),
                    'photos': place.get('photos', []),
                    'geometry': place.get('geometry', {}),
                    'formatted_address': place.get('formatted_address'),
                    'price_level': place.get('price_level'),
                    'types': place.get('types', [])
                }
        except Exception as e:
            print(f"Error searching place: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def get_place_photos(self, place_id: str, max_photos: int = 1) -> List[str]:
        """Get photo URLs for a place using place_id"""
        if not self.client:
            return []
        
        try:
            # Get place details with photos field
            place_details = self.client.place(
                place_id=place_id,
                fields=['photos', 'name']
            )
            
            photos = place_details.get('result', {}).get('photos', [])
            photo_urls = []
            
            for photo in photos[:max_photos]:
                # Get photo reference
                photo_reference = photo.get('photo_reference')
                if photo_reference:
                    # Build photo URL - Google Places Photo API
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={self.api_key}"
                    photo_urls.append(photo_url)
            
            return photo_urls
        except Exception as e:
            print(f"Error getting place photos: {e}")
            import traceback
            traceback.print_exc()
        
        return []
    
    def get_photo_from_place_data(self, place_data: Dict) -> Optional[str]:
        """Extract photo URL from place search result"""
        if not self.client or not place_data:
            return None
        
        photos = place_data.get('photos', [])
        if photos:
            photo_reference = photos[0].get('photo_reference')
            if photo_reference:
                return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={self.api_key}"
        
        return None
    
    def get_restaurant_photo(self, restaurant_name: str, location: str) -> Optional[str]:
        """Get a photo for a restaurant by searching for it"""
        if not self.client:
            # Fallback: Return Unsplash food image
            return self._get_fallback_food_image(restaurant_name)
        
        try:
            place_data = self.search_place_by_name(restaurant_name, location)
            if place_data:
                photo_url = self.get_photo_from_place_data(place_data)
                if photo_url:
                    return photo_url
        except Exception as e:
            print(f"Error getting restaurant photo: {e}")
        
        # Fallback: Return Unsplash food image
        return self._get_fallback_food_image(restaurant_name)
    
    def _get_fallback_food_image(self, restaurant_name: str) -> str:
        """Get a fallback food image from Unsplash"""
        # Use Unsplash Source API for food images
        # This is a free service that provides food-related images
        search_term = "restaurant food".replace(" ", "+")
        return f"https://source.unsplash.com/400x300/?{search_term}"
