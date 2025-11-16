# Database models (placeholders for future database integration)
# This file will contain SQLAlchemy models or similar database models

class Restaurant:
    """Restaurant data model"""
    def __init__(self, id, name, address, latitude, longitude, rating, budget):
        self.id = id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.rating = rating
        self.budget = budget
        self.cuisines = []
        self.image = None
        self.website = None
        self.menu_link = None
        self.phone = None
        self.hours = {}
        self.accessibility = []
        self.service_types = []
        self.matching_items = []
