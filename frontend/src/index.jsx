import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Suppress WebSocket dev server errors
const originalError = console.error;
console.error = (...args) => {
  if (args[0]?.includes?.('WebSocket') || args[0]?.includes?.('ws://')) {
    return; // Suppress WebSocket connection errors
  }
  originalError(...args);
};

// Load Google Maps API
const loadGoogleMapsAPI = () => {
  const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
  if (!apiKey) {
    console.warn('⚠️ REACT_APP_GOOGLE_MAPS_API_KEY is not set in .env');
    return;
  }
  
  // Only attempt to load if we have a valid key
  if (apiKey === '<GOOGLE_MAPS_API_KEY>' || apiKey.length < 20) {
    console.warn('⚠️ Invalid Google Maps API key format - map will not load');
    return;
  }
  
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
  script.async = true;
  script.defer = true;
  script.onerror = (error) => {
    console.error('⚠️ Google Maps API error - map will not display.');
    console.error('To fix: Enable "Maps JavaScript API" in Google Cloud Console');
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
