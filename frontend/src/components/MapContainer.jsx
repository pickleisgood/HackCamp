import React, { useEffect } from 'react';
import '../styles/MapContainer.css';

function MapContainer({ restaurants, center = { lat: 40.7128, lng: -74.0060 } }) {
  const mapRef = React.useRef(null);
  const [map, setMap] = React.useState(null);
  const markersRef = React.useRef([]);

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize map
    const googleMap = new window.google.maps.Map(mapRef.current, {
      zoom: 13,
      center: {
        lat: (center && center.lat) || 40.7128,
        lng: (center && center.lng) || -74.0060
      },
      mapTypeId: window.google.maps.MapTypeId.ROADMAP
    });

    setMap(googleMap);
  }, [center?.lat, center?.lng]);

  useEffect(() => {
    if (!map) return;

    console.log(`📍 Map updating with ${restaurants.length} restaurants`);

    // Clear existing markers
    markersRef.current.forEach(marker => marker.setMap(null));
    markersRef.current = [];

    // Add markers for each restaurant with animation
    restaurants.forEach((restaurant, index) => {
      if (restaurant.latitude && restaurant.longitude) {
        const marker = new window.google.maps.Marker({
          position: {
            lat: parseFloat(restaurant.latitude),
            lng: parseFloat(restaurant.longitude)
          },
          map: map,
          title: restaurant.name,
          label: String(index + 1),
          animation: window.google.maps.Animation.DROP
        });

        // Add info window with restaurant details and dietary info
        const dietaryInfo = restaurant.dietary_accommodation 
          ? `<p style="margin: 4px 0; font-size: 11px; color: #2ecc71; font-weight: bold;">✓ ${restaurant.dietary_accommodation}</p>`
          : '';
        
        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div class="map-popup" style="max-width: 280px; padding: 12px; font-family: Arial, sans-serif;">
              <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold;">${restaurant.name}</h3>
              <p style="margin: 4px 0; font-size: 12px;">${restaurant.address}</p>
              <p style="margin: 4px 0; font-size: 12px;">⭐ ${restaurant.rating || 'N/A'} ${restaurant.budget ? ' • ' + restaurant.budget : ''}</p>
              ${restaurant.phone ? `<p style="margin: 4px 0; font-size: 12px;">📞 ${restaurant.phone}</p>` : ''}
              ${dietaryInfo}
            </div>
          `
        });

        marker.addListener('click', () => {
          infoWindow.open(map, marker);
        });

        markersRef.current.push(marker);
      }
    });

    // Fit map bounds to show all markers with animation
    if (markersRef.current.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      markersRef.current.forEach(marker => {
        bounds.extend(marker.getPosition());
      });
      map.fitBounds(bounds, { top: 50, right: 50, bottom: 50, left: 50 });
    }
  }, [map, restaurants]);

  return (
    <div className="map-container">
      <div ref={mapRef} className="map-inner" style={{ width: '100%', height: '100%' }} />
      {restaurants.length === 0 && (
        <div className="map-placeholder">
          <p>Search for restaurants to see them on the map</p>
        </div>
      )}
    </div>
  );
}

export default MapContainer;
