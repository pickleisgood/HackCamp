import React from 'react';
import '../styles/LoadingPopup.css';

function LoadingPopup({ isVisible, message = 'Searching for restaurants...' }) {
  if (!isVisible) return null;

  return (
    <div className="loading-popup-backdrop">
      <div className="loading-popup">
        <div className="loading-spinner"></div>
        <h2>🤖 AI Agent Searching</h2>
        <p>{message}</p>
        <div className="loading-progress">
          <div className="progress-bar"></div>
        </div>
        <p className="loading-hint">This may take a moment...</p>
      </div>
    </div>
  );
}

export default LoadingPopup;
