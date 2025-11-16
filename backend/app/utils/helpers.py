# Utility functions for common operations

def parse_rating_filter(rating_str: str) -> float:
    """Parse rating string to float"""
    if rating_str.endswith('+'):
        return float(rating_str[:-1])
    return float(rating_str)

def format_budget(budget_level: str) -> str:
    """Format budget level to consistent format"""
    budget_map = {
        '$': 1,
        '$$': 2,
        '$$$': 3,
        '$$$$': 4,
    }
    return budget_map.get(budget_level, 0)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers"""
    import math
    R = 6371  # Earth's radius in km
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def validate_filters(filters: dict) -> dict:
    """Validate and sanitize filter inputs"""
    validated = {}
    if 'minRating' in filters:
        validated['minRating'] = max(0, min(5, float(filters.get('minRating', 3.5))))
    validated['budget'] = filters.get('budget', [])
    validated['dietary'] = filters.get('dietary', [])
    validated['cuisines'] = filters.get('cuisines', [])
    validated['serviceType'] = filters.get('serviceType', [])
    validated['accessibility'] = filters.get('accessibility', [])
    validated['operational'] = filters.get('operational', [])
    return validated
