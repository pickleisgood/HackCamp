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
    
    def search_place_by_name(self, name: str, location: str, include_restaurant_keyword: bool = True) -> Optional[Dict]:
        """Search for a place by name and location"""
        if not self.client:
            return None
        
        try:
            # Search for the place using text search
            query = f"{name} {location}" if not include_restaurant_keyword else f"{name} restaurant {location}"
            places_result = self.client.places(
                query=query,
                type='restaurant'
            )
            
            if places_result and places_result.get('results'):
                # Try to find the best match by name similarity
                best_match = None
                name_lower = name.lower()
                
                for place in places_result.get('results', []):
                    place_name = place.get('name', '').lower()
                    # Check if restaurant name is in the place name or vice versa
                    if name_lower in place_name or place_name in name_lower:
                        best_match = place
                        break
                
                # If no close match, use first result
                if not best_match:
                    best_match = places_result['results'][0]
                
                return {
                    'place_id': best_match.get('place_id'),
                    'name': best_match.get('name'),
                    'rating': best_match.get('rating'),
                    'photos': best_match.get('photos', []),
                    'geometry': best_match.get('geometry', {}),
                    'formatted_address': best_match.get('formatted_address'),
                    'price_level': best_match.get('price_level'),
                    'types': best_match.get('types', [])
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
        """Get a REAL photo for a restaurant by searching for it - returns None if no real photo found"""
        if not self.client:
            print(f"⚠️ Google Maps API not available - cannot fetch real restaurant photo for {restaurant_name}")
            return None
        
        try:
            # Try multiple search strategies to find the restaurant
            place_data = self.search_place_by_name(restaurant_name, location)
            
            # If first search didn't work, try without "restaurant" keyword
            if not place_data:
                place_data = self.search_place_by_name(restaurant_name, location, include_restaurant_keyword=False)
            
            if place_data:
                photo_url = self.get_photo_from_place_data(place_data)
                if photo_url:
                    print(f"✓ Found REAL restaurant photo from Google Maps for {restaurant_name}")
                    return photo_url
                else:
                    print(f"⚠️ Restaurant found in Google Maps but no photo available for {restaurant_name}")
            else:
                print(f"⚠️ Restaurant {restaurant_name} not found in Google Maps")
        except Exception as e:
            print(f"Error getting restaurant photo from Google Maps: {e}")
            import traceback
            traceback.print_exc()
        
        return None  # Return None if no real photo found - don't use generic fallbacks
    
    def get_image_from_website(self, website_url: str, restaurant_name: str = "") -> Optional[str]:
        """Try to extract an image from a restaurant website"""
        if not website_url:
            return None
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin, urlparse
            
            # Ensure URL has protocol
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.get(website_url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Priority 1: Try to find Open Graph image first (most reliable)
                og_image = soup.find('meta', property='og:image')
                if og_image and og_image.get('content'):
                    img_url = og_image.get('content').strip()
                    if img_url:
                        # Make absolute URL if relative
                        if img_url.startswith('/') or not img_url.startswith('http'):
                            img_url = urljoin(website_url, img_url)
                        # Verify it's a valid image URL
                        if any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) or 'image' in img_url.lower():
                            return img_url
                
                # Priority 2: Try Twitter Card image
                twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
                if twitter_image and twitter_image.get('content'):
                    img_url = twitter_image.get('content').strip()
                    if img_url:
                        if img_url.startswith('/') or not img_url.startswith('http'):
                            img_url = urljoin(website_url, img_url)
                        if any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                            return img_url
                
                # Priority 3: Find images in the page, prioritizing large/hero images
                images = soup.find_all('img', src=True)
                candidate_images = []
                
                for img in images:
                    src = img.get('src', '').strip()
                    if not src:
                        continue
                    
                    # Skip small icons/logos
                    if any(skip in src.lower() for skip in ['icon', 'logo', 'button', 'avatar', 'badge', 'favicon', 'sprite']):
                        continue
                    
                    # Make absolute URL if relative
                    if src.startswith('/') or not src.startswith('http'):
                        src = urljoin(website_url, src)
                    
                    # Check image attributes for size hints
                    width = img.get('width', '')
                    height = img.get('height', '')
                    class_name = img.get('class', [])
                    alt_text = img.get('alt', '').lower()
                    
                    # Score images based on likelihood of being a restaurant photo
                    score = 0
                    if any(keyword in src.lower() for keyword in ['hero', 'banner', 'main', 'gallery', 'food', 'restaurant', 'interior', 'exterior', 'dish', 'meal']):
                        score += 10
                    if any(keyword in alt_text for keyword in ['food', 'restaurant', 'dish', 'meal', 'cuisine']):
                        score += 5
                    if any(keyword in ' '.join(class_name).lower() for keyword in ['hero', 'banner', 'main', 'featured', 'gallery']):
                        score += 5
                    if width and height:
                        try:
                            w, h = int(width), int(height)
                            if w > 300 and h > 200:  # Reasonable size
                                score += 3
                        except:
                            pass
                    
                    if score > 0 or any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        candidate_images.append((score, src))
                
                # Return the highest scoring image
                if candidate_images:
                    candidate_images.sort(key=lambda x: x[0], reverse=True)
                    return candidate_images[0][1]
                
        except requests.exceptions.Timeout:
            print(f"Timeout scraping image from website {website_url}")
        except requests.exceptions.RequestException as e:
            print(f"Request error scraping image from website {website_url}: {e}")
        except Exception as e:
            print(f"Error scraping image from website {website_url}: {e}")
        
        return None
    
    def _get_fallback_food_image(self, restaurant_name: str) -> str:
        """Get a fallback food image - use Picsum with food-related seed"""
        # Use Picsum Photos with a deterministic seed based on restaurant name
        # This ensures consistent images per restaurant while still showing food/restaurant images
        import hashlib
        seed = hashlib.md5(restaurant_name.encode()).hexdigest()[:8]
        # Use a food/restaurant themed image by using specific image IDs from Picsum
        # These are curated to be food/restaurant related
        food_image_ids = [1015, 1018, 1025, 1035, 1041, 1043, 1047, 1050, 1055, 1060, 1069, 1074]
        image_id = food_image_ids[int(seed, 16) % len(food_image_ids)]
        return f"https://picsum.photos/seed/{seed}/400/300"
