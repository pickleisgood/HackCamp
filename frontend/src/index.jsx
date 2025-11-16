import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Load Google Maps API
const loadGoogleMapsAPI = () => {
  const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
  if (!apiKey) {
    console.warn('⚠️ REACT_APP_GOOGLE_MAPS_API_KEY is not set in .env');
    return;
  }
  
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
  script.async = true;
  script.defer = true;
  script.onerror = (error) => {
    console.error('❌ Failed to load Google Maps API:', error);
    console.error('API Key:', apiKey);
  };
  script.onload = () => {
    console.log('✓ Google Maps API loaded successfully');
  };
  document.head.appendChild(script);
};

// Load Google Maps before rendering
loadGoogleMapsAPI();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
