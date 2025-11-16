import React, { useState } from 'react';
import '../styles/FilterOverlay.css';

function FilterOverlay({ onApply, onClose }) {
  const [filters, setFilters] = useState({
    budget: [],
    dietary: [],
    cuisines: [],
    minRating: 3.5,
    serviceType: [],
    accessibility: [],
    operational: [],
  });

  const budgetOptions = ['$', '$$', '$$$', '$$$$'];
  const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Halal', 'Kosher'];
  const cuisineOptions = ['Italian', 'Asian', 'Mexican', 'Indian', 'American', 'French'];
  const serviceTypes = ['Dine-In', 'Takeout', 'Delivery'];
  const accessibilityOptions = ['Wheelchair Accessible', 'Accessible Washroom', 'Allergen Menu'];
  const operationalOptions = ['Open Now', 'Open Late', 'Breakfast', 'Lunch', 'Dinner'];
  const ratingOptions = [3.5, 4.0, 4.5];

  const handleFilterChange = (category, value) => {
    setFilters(prev => ({
      ...prev,
      [category]: prev[category].includes(value)
        ? prev[category].filter(item => item !== value)
        : [...prev[category], value]
    }));
  };

  const handleRatingChange = (value) => {
    setFilters(prev => ({
      ...prev,
      minRating: value
    }));
  };

  const handleApply = () => {
    onApply(filters);
  };

  return (
    <div className="filter-overlay-backdrop" onClick={onClose}>
      <div className="filter-overlay" onClick={(e) => e.stopPropagation()}>
        <div className="filter-header">
          <h2>Filters</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="filter-content">
          {/* Budget Filter */}
          <div className="filter-group">
            <h3>Budget</h3>
            <div className="filter-options">
              {budgetOptions.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.budget.includes(option)}
                    onChange={() => handleFilterChange('budget', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Dietary Restrictions */}
          <div className="filter-group">
            <h3>Dietary Restrictions</h3>
            <div className="filter-options">
              {dietaryOptions.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.dietary.includes(option)}
                    onChange={() => handleFilterChange('dietary', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Cuisines */}
          <div className="filter-group">
            <h3>Cuisines</h3>
            <div className="filter-options">
              {cuisineOptions.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.cuisines.includes(option)}
                    onChange={() => handleFilterChange('cuisines', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Service Type */}
          <div className="filter-group">
            <h3>Service Type</h3>
            <div className="filter-options">
              {serviceTypes.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.serviceType.includes(option)}
                    onChange={() => handleFilterChange('serviceType', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Accessibility */}
          <div className="filter-group">
            <h3>Accessibility</h3>
            <div className="filter-options">
              {accessibilityOptions.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.accessibility.includes(option)}
                    onChange={() => handleFilterChange('accessibility', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Operational */}
          <div className="filter-group">
            <h3>Operational Hours</h3>
            <div className="filter-options">
              {operationalOptions.map(option => (
                <label key={option}>
                  <input
                    type="checkbox"
                    checked={filters.operational.includes(option)}
                    onChange={() => handleFilterChange('operational', option)}
                  />
                  {option}
                </label>
              ))}
            </div>
          </div>

          {/* Minimum Rating */}
          <div className="filter-group">
            <h3>Minimum Rating</h3>
            <div className="filter-options">
              {ratingOptions.map(option => (
                <label key={option}>
                  <input
                    type="radio"
                    name="rating"
                    value={option}
                    checked={filters.minRating === option}
                    onChange={() => handleRatingChange(option)}
                  />
                  {option}+
                </label>
              ))}
            </div>
          </div>
        </div>

        <div className="filter-actions">
          <button className="apply-button" onClick={handleApply}>Apply Filters</button>
          <button className="reset-button" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default FilterOverlay;
