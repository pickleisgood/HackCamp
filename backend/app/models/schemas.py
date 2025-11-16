from pydantic import BaseModel
from typing import List, Optional

class FilterRequest(BaseModel):
    budget: Optional[List[str]] = []
    dietary: Optional[List[str]] = []
    cuisines: Optional[List[str]] = []
    minRating: Optional[float] = 3.5
    serviceType: Optional[List[str]] = []
    accessibility: Optional[List[str]] = []
    operational: Optional[List[str]] = []

class SearchRequest(BaseModel):
    location: str
    filters: Optional[FilterRequest] = None
    radius: Optional[int] = 5000  # in meters

class RestaurantResponse(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    rating: float
    budget: str
    cuisines: List[str]
    image: Optional[str] = None
    website: Optional[str] = None
    menuLink: Optional[str] = None
    matchingItems: Optional[List[str]] = []
    phone: Optional[str] = None
    hours: Optional[dict] = None
    accessibility: Optional[List[str]] = []
    serviceTypes: Optional[List[str]] = []

class SearchResponse(BaseModel):
    totalFound: int
    restaurants: List[RestaurantResponse]
    location: str
    filters: Optional[FilterRequest] = None
