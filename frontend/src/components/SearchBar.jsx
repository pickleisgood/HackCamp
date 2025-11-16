import React, { useState } from 'react';
import '../styles/SearchBar.css';

function SearchBar({ onSearch, currentFilters = null }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      // Pass the location and current filters to ensure both are used
      onSearch(input, currentFilters);
    } else {
      alert('Please enter a location to search for restaurants.');
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter your location..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="search-input"
      />
      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}

export default SearchBar;
