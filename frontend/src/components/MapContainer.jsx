import React from 'react';
import '../styles/MapContainer.css';

function MapContainer({ restaurants, center }) {
  // TODO: Integrate @react-google-maps/api
  // This is a placeholder component
  return (
    <div className="map-container">
      <div className="map-placeholder">
        <p>Google Maps will be embedded here</p>
        <p>Center: {center.lat}, {center.lng}</p>
        <p>Restaurants to display: {restaurants.length}</p>
      </div>
    </div>
  );
}

export default MapContainer;
