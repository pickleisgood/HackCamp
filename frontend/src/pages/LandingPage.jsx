import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import FilterOverlay from '../components/FilterOverlay';
import LoadingPopup from '../components/LoadingPopup';
import MapContainer from '../components/MapContainer';
import RestaurantList from '../components/RestaurantList';
import { searchRestaurants } from '../utils/api';
import '../styles/LandingPage.css';

function LandingPage() {
  const [location, setLocation] = useState('');
  const [filters, setFilters] = useState({});
  const [restaurants, setRestaurants] = useState([]);
  const [showFilterOverlay, setShowFilterOverlay] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState({ lat: 40.7128, lng: -74.0060 });

  const handleSearch = async (searchLocation, searchFilters = null) => {
    // Use provided location or current location state
    const locationToUse = searchLocation || location;
    // Use provided filters or current filters state
    const filtersToUse = searchFilters !== null ? searchFilters : filters;
    
    // Update state with the values being used
    if (searchLocation) {
      setLocation(searchLocation);
    }
    if (searchFilters !== null) {
      setFilters(searchFilters);
    }
    
    // Validate location is provided
    if (!locationToUse || !locationToUse.trim()) {
      alert('Please enter a location to search for restaurants.');
      return;
    }
    
    setLoading(true);
    try {
      // Call backend API with current location and current filters (including dietary restrictions)
      console.log('🔍 Searching with:', { location: locationToUse, filters: filtersToUse });
      const response = await searchRestaurants(locationToUse, filtersToUse);
      
      if (response.restaurants && response.restaurants.length > 0) {
        setRestaurants(response.restaurants);
        // Update map center to first restaurant or use geocoded location
        if (response.restaurants[0]) {
          setMapCenter({
            lat: response.restaurants[0].latitude,
            lng: response.restaurants[0].longitude
          });
        }
      } else {
        setRestaurants([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Error searching restaurants. Please try again.');
      setRestaurants([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setShowFilterOverlay(false);
    
    // Auto-search with new filters if location is set
    // Pass the new filters explicitly to ensure they're used
    if (location.trim()) {
      handleSearch(location, newFilters);
    }
  };

  const formatFiltersSummary = () => {
    const counts = Object.values(filters).reduce((count, value) => {
      if (Array.isArray(value)) return count + value.length;
      return count;
    }, 0);
    return counts > 0 ? `${counts} filters active` : 'No filters';
  };

  return (
    <div className="landing-page">
      {/* Logo in top left corner */}
      <div className="logo-container">
        <img src="/logo.png" alt="Logo" className="logo" />
      </div>

      {/* Loading Popup */}
      <LoadingPopup 
        isVisible={loading} 
        message="🤖 AI Agent searching for perfect restaurants matching your preferences..."
      />

      {/* Search Section */}
      <div className="search-section">
        <h1>🍽️ Find Your Perfect Restaurant</h1>
        <p className="subtitle">Powered by AI • Personalized to Your Taste</p>
        <SearchBar onSearch={handleSearch} currentFilters={filters} />
        
        <div className="search-controls">
          <button 
            className="filter-button"
            onClick={() => setShowFilterOverlay(!showFilterOverlay)}
          >
            🔧 Refine Search
          </button>
          <span className="filter-status">
            {formatFiltersSummary()}
          </span>
        </div>
      </div>

      {/* Filter Overlay */}
      {showFilterOverlay && (
        <FilterOverlay 
          onApply={handleFilterChange}
          onClose={() => setShowFilterOverlay(false)}
          initialFilters={filters}
        />
      )}

      {/* Main Content */}
      <div className="main-content">
        <div className="map-section">
          <MapContainer 
            restaurants={restaurants}
            center={mapCenter}
          />
        </div>

        <div className="results-section">
          <div className="results-header">
            <h2>
              {loading 
                ? '⏳ Searching...' 
                : restaurants.length > 0 
                  ? `✓ Found ${restaurants.length} restaurants` 
                  : '🔍 Search to discover restaurants'}
            </h2>
            {restaurants.length > 0 && (
              <span className="result-count-badge">{restaurants.length}</span>
            )}
          </div>
          
          <RestaurantList 
            restaurants={restaurants}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
