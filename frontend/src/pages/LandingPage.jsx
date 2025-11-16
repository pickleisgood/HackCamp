import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import FilterOverlay from '../components/FilterOverlay';
import MapContainer from '../components/MapContainer';
import RestaurantList from '../components/RestaurantList';
import '../styles/LandingPage.css';

function LandingPage() {
  const [location, setLocation] = useState('');
  const [filters, setFilters] = useState({});
  const [restaurants, setRestaurants] = useState([]);
  const [showFilterOverlay, setShowFilterOverlay] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState({ lat: 40.7128, lng: -74.0060 });

  const handleSearch = async (searchLocation) => {
    setLocation(searchLocation);
    setLoading(true);
    // TODO: Call backend API to search restaurants
    setLoading(false);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setShowFilterOverlay(false);
    // TODO: Re-fetch restaurants with new filters
  };

  return (
    <div className="landing-page">
      <div className="search-section">
        <h1>Find Your Perfect Restaurant</h1>
        <SearchBar onSearch={handleSearch} />
        <button 
          className="filter-button"
          onClick={() => setShowFilterOverlay(!showFilterOverlay)}
        >
          🔧 Filters
        </button>
      </div>

      {showFilterOverlay && (
        <FilterOverlay 
          onApply={handleFilterChange}
          onClose={() => setShowFilterOverlay(false)}
        />
      )}

      <div className="main-content">
        <div className="map-section">
          <MapContainer 
            restaurants={restaurants}
            center={mapCenter}
          />
        </div>

        <div className="results-section">
          <h2>
            {restaurants.length > 0 
              ? `Found ${restaurants.length} restaurants` 
              : 'No restaurants found'}
          </h2>
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
