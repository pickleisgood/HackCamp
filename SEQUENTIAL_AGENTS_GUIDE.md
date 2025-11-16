# 🤖 Sequential Gemini Agents - Architecture Guide

## Overview

The restaurant finder now uses **sequential AI agents** to search for restaurants and transform data for frontend display. This two-stage approach ensures accurate results and proper data formatting.

## Architecture

### Two-Agent Sequential Pipeline

```
User Request
    ↓
    ├─ STAGE 1: Web Scraper Agent ──→ Raw Restaurant Data
    │
    └─ STAGE 2: Data Transformer Agent ──→ Formatted & Filtered Results
    
    ↓
    Frontend Display
```

## Agent Details

### Agent 1: WebScraperAgent

**Purpose**: Find real restaurants matching search criteria

**Responsibilities**:
- ✅ Search for actual restaurants in the location
- ✅ Convert filter criteria to web search queries
- ✅ Generate realistic restaurant data based on filters
- ✅ Return raw restaurant information (names, addresses, cuisine, etc.)

**Methods**:
- `search_restaurants_web(location, filters)` - Main search method
- `_build_search_query(location, filters)` - Convert filters to search query
- `_search_google_places_equivalent(location, filters)` - Search via API
- `_generate_restaurant_data(location, filters, search_query)` - Generate realistic data

**Output Format**:
```json
{
  "raw_results": [
    {
      "name": "Restaurant Name",
      "address": "Address",
      "cuisine": ["Type1"],
      "rating": 4.5,
      "budget": "$$",
      "hours": "Mon-Sun 11am-11pm",
      "menu_items": ["Item1", "Item2"],
      "service_types": ["Dine-in", "Takeout"]
    }
  ],
  "search_query": "San Francisco Italian Vegetarian",
  "total_found": 8,
  "status": "success"
}
```

---

### Agent 2: DataTransformerAgent

**Purpose**: Transform raw data into frontend-displayable format

**Responsibilities**:
- ✅ Filter restaurants against ALL user criteria
- ✅ Calculate match scores (0-100)
- ✅ Identify matching menu items for dietary restrictions
- ✅ Extract accessibility features
- ✅ Add location coordinates
- ✅ Provide explanations for why restaurants match
- ✅ Sort by relevance (match score)

**Methods**:
- `transform_restaurant_data(raw_restaurants, filters)` - Main transformation method

**Output Format**:
```json
{
  "transformed_restaurants": [
    {
      "id": "unique_id",
      "name": "Restaurant Name",
      "address": "Full Address",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "rating": 4.5,
      "budget": "$$",
      "cuisines": ["Italian"],
      "match_score": 95,
      "matching_menu_items": ["Pasta Primavera", "Vegetable Risotto"],
      "why_it_matches": "Perfect for vegetarians with Italian cuisine",
      "accessibility_features": ["Wheelchair Access"],
      "service_types": ["Dine-in", "Takeout"],
      "tags": ["vegetarian-friendly", "italian", "upscale-casual"]
    }
  ],
  "total_matching": 5,
  "search_summary": "Found 5 restaurants matching your criteria"
}
```

---

## Main Service: GeminiAgentService

**Purpose**: Orchestrate the two agents

**Key Method**: `search_restaurants(location, filters)`

### Workflow

```
1. Initialize both agents
2. Call WebScraperAgent.search_restaurants_web()
   ↓ Get: Raw restaurant data (names, addresses, cuisines, etc.)
3. Call DataTransformerAgent.transform_restaurant_data()
   ↓ Get: Formatted, filtered, scored restaurants
4. Return: Final results for frontend
```

### Example Response

```json
{
  "restaurants": [
    {
      "id": "restaurant_1",
      "name": "Locanda Positano",
      "address": "123 Grant Ave, San Francisco, CA 94108",
      "latitude": 37.7949,
      "longitude": -122.4076,
      "rating": 4.7,
      "budget": "$$",
      "cuisines": ["Italian"],
      "website": "https://locandapositano.com",
      "phone": "(415) 986-7771",
      "hours": "Mon-Sun 11:30am-10pm",
      "match_score": 98,
      "matching_menu_items": [
        "Pasta Primavera",
        "Vegetable Risotto",
        "Eggplant Parmesan"
      ],
      "why_it_matches": "Excellent vegetarian Italian restaurant with high rating and upscale pricing",
      "accessibility_features": ["Wheelchair Access", "Accessible Restrooms"],
      "service_types": ["Dine-in", "Takeout"],
      "tags": ["vegetarian", "italian", "upscale"]
    },
    {
      "id": "restaurant_2",
      "name": "Flour + Water",
      "address": "2401 Harrison St, San Francisco, CA 94110",
      "latitude": 37.7624,
      "longitude": -122.4119,
      "rating": 4.5,
      "budget": "$$",
      "cuisines": ["Italian"],
      "website": "https://flourandwater.com",
      "phone": "(415) 641-4555",
      "hours": "Tue-Sun 5pm-11pm",
      "match_score": 92,
      "matching_menu_items": [
        "Handmade Pasta with Vegetables",
        "Seasonal Vegetable Dishes"
      ],
      "why_it_matches": "Known for vegetable-focused Italian cuisine with modern approach",
      "accessibility_features": ["Wheelchair Access"],
      "service_types": ["Dine-in"],
      "tags": ["vegetarian", "italian", "modern"]
    }
  ],
  "totalFound": 2,
  "searchSummary": "Found 2 restaurants matching your criteria",
  "filters_applied": {
    "budget": ["$$", "$$$"],
    "dietary": ["Vegetarian"],
    "cuisines": ["Italian"],
    "minRating": 4.0
  }
}
```

---

## Filter Flow

### Filters Sent by Frontend

```json
{
  "budget": ["$$", "$$$"],
  "dietary": ["Vegetarian"],
  "cuisines": ["Italian", "Mediterranean"],
  "minRating": 4.0,
  "serviceType": ["Dine-in", "Takeout"],
  "accessibility": ["Wheelchair Accessible"],
  "operational": []
}
```

### How Filters Are Applied

1. **WebScraperAgent** converts filters to search query:
   - "San Francisco Italian Mediterranean Vegetarian $$"

2. **WebScraperAgent** finds restaurants with those criteria

3. **DataTransformerAgent** validates EVERY restaurant against ALL filters:
   - ✅ Budget matches one of the selected options
   - ✅ Has vegetarian menu items
   - ✅ Serves Italian or Mediterranean
   - ✅ Rating ≥ 4.0
   - ✅ Offers selected service types
   - ✅ Has accessibility features (if selected)

4. **DataTransformerAgent** calculates match score:
   - 100 = perfect match on all criteria
   - Lower scores = matches some but not all criteria

5. **DataTransformerAgent** sorts by match score (highest first)

---

## Integration with Frontend

### What Frontend Receives

For each restaurant:
- ✅ **Basic Info**: name, address, rating, budget
- ✅ **Location**: latitude, longitude (for maps)
- ✅ **Menu**: matching_menu_items (dishes matching dietary)
- ✅ **Match Score**: 0-100 indicating relevance
- ✅ **Explanation**: why_it_matches (why this restaurant matches)
- ✅ **Accessibility**: accessibility_features list
- ✅ **Tags**: semantic tags for filtering/UI

### Frontend Display

```
Restaurant Card:
┌─────────────────────────────────┐
│ Locanda Positano ⭐ 4.7         │
│ 123 Grant Ave, SF               │
│ Italian • $$ • Match Score: 98% │
│                                 │
│ Why it matches:                 │
│ "Excellent vegetarian Italian   │
│  restaurant with high rating"   │
│                                 │
│ Vegetarian options:             │
│ • Pasta Primavera               │
│ • Vegetable Risotto             │
│ • Eggplant Parmesan             │
│                                 │
│ ♿ Wheelchair Access             │
│ 🍽️  Dine-in • 📦 Takeout        │
└─────────────────────────────────┘
```

---

## Advantages of Sequential Agents

✅ **Separation of Concerns**
- WebScraper: Finding real data
- Transformer: Formatting & filtering

✅ **Accuracy**
- Two levels of filtering ensure correct results
- Each agent specializes in its task

✅ **Transparency**
- Match scores show why restaurants were selected
- Explanations help users understand relevance

✅ **Flexibility**
- Easy to add more agents (e.g., ReviewAgent, PricingAgent)
- Each agent can be improved independently

✅ **Reproducibility**
- Same search produces consistent results
- Full audit trail of decision-making

---

## Testing

### Run Test Script

```bash
cd /Users/andrexue/GitHub/HackCamp/backend
python3 test_agents.py
```

### Expected Output

```
======================================================================
🚀 TESTING SEQUENTIAL AGENTS
======================================================================

Searching for restaurants in: San Francisco, CA
Filters: {...}

======================================================================
📍 STEP 1: Web Scraper Agent
----------------------------------------------------------------------
🌐 Web Scraper Agent: Searching for restaurants in San Francisco, CA
✓ Found 8 raw restaurant results

======================================================================
📍 STEP 2: Data Transformer Agent
----------------------------------------------------------------------
🔄 Data Transformer Agent: Processing 8 restaurants
✓ Transformed into 5 displayable restaurants

======================================================================
✅ SEARCH COMPLETE
======================================================================

📊 RESULTS
======================================================================

Total Found: 5
Search Summary: Found 5 restaurants matching your criteria

✅ Found 5 restaurants:

1. Locanda Positano
   Address: 123 Grant Ave, San Francisco, CA
   Rating: 4.7 stars
   Budget: $$
   Match Score: 98/100
   Why It Matches: Excellent vegetarian Italian restaurant...
   Menu Items: Pasta Primavera, Vegetable Risotto, ...
```

---

## Error Handling

### No Results

```json
{
  "restaurants": [],
  "error": "No restaurants found matching your criteria",
  "searchSummary": "Search returned no results"
}
```

### Transformation Error

```json
{
  "transformed_restaurants": [],
  "error": "Failed to transform restaurant data",
  "search_summary": "No results could be processed"
}
```

---

## Future Enhancements

1. **Review Agent**: Scrape customer reviews
2. **Pricing Agent**: Get real-time pricing
3. **Menu Agent**: Extract detailed menus
4. **Rating Agent**: Get up-to-date ratings
5. **Database Agent**: Cache results for speed
6. **Personalization Agent**: Learn from user choices

---

## Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash-lite  # or gemini-2.5-flash
```

### Model Selection

- **Fast**: `gemini-2.5-flash-lite`
- **Better**: `gemini-2.5-flash`
- **Best**: `gemini-pro` (requires paid tier)

---

## Troubleshooting

### No Restaurants Returned

1. Check filters are valid
2. Verify location string is clear (e.g., "San Francisco, CA")
3. Check API key is set correctly
4. Check internet connection

### Match Scores Too Low

1. Reduce filter criteria (too restrictive)
2. Lower minimum rating requirement
3. Add more budget options

### API Rate Limits

1. Reduce search frequency
2. Cache results
3. Upgrade API tier

---

**Sequential agents provide transparent, accurate, and explainable restaurant recommendations!** 🎉
