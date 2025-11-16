import React, { useState, useEffect } from 'react';
import '../styles/FilterOverlay.css';

function FilterOverlay({ onApply, onClose, initialFilters = {} }) {
  const [filters, setFilters] = useState({
    budget: initialFilters.budget || [],
    dietary: initialFilters.dietary || [],
    cuisines: initialFilters.cuisines || [],
    minRating: initialFilters.minRating || 3.5,
    serviceType: initialFilters.serviceType || [],
    accessibility: initialFilters.accessibility || [],
    operational: initialFilters.operational || [],
  });

  // Budget with clear labels
  const budgetOptions = [
    { value: '$', label: '$ - Budget Friendly (Under $15/person)' },
    { value: '$$', label: '$$ - Moderate ($15-$30/person)' },
    { value: '$$$', label: '$$$ - Upscale ($30-$60/person)' },
    { value: '$$$$', label: '$$$$ - Fine Dining ($60+/person)' }
  ];

  const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Halal', 'Kosher'];
  const cuisineOptions = ['Italian', 'Asian', 'Mexican', 'Indian', 'American', 'French', 'Mediterranean', 'Thai', 'Japanese'];
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

  const handleReset = () => {
    setFilters({
      budget: [],
      dietary: [],
      cuisines: [],
      minRating: 3.5,
      serviceType: [],
      accessibility: [],
      operational: [],
    });
  };

  // Count active filters
  const activeFilterCount = Object.values(filters).reduce((count, value) => {
    if (Array.isArray(value)) return count + value.length;
    return count;
  }, 0);

  return (
    <div className="filter-overlay-backdrop" onClick={onClose}>
      <div className="filter-overlay" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="filter-header">
          <div className="filter-title-section">
            <h2>🔍 Search Filters</h2>
            {activeFilterCount > 0 && (
              <span className="active-count-badge">{activeFilterCount} Active</span>
            )}
          </div>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {/* Content */}
        <div className="filter-content">
          {/* Budget Filter */}
          <div className="filter-group">
            <h3>💰 Budget</h3>
            <div className="filter-options">
              {budgetOptions.map(option => (
                <label key={option.value} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.budget.includes(option.value)}
                    onChange={() => handleFilterChange('budget', option.value)}
                  />
                  <span className="label-text">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Dietary Restrictions */}
          <div className="filter-group">
            <h3>🥗 Dietary Restrictions</h3>
            <div className="filter-options">
              {dietaryOptions.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.dietary.includes(option)}
                    onChange={() => handleFilterChange('dietary', option)}
                  />
                  <span className="label-text">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Cuisines */}
          <div className="filter-group">
            <h3>🍽️ Cuisines</h3>
            <div className="filter-options">
              {cuisineOptions.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.cuisines.includes(option)}
                    onChange={() => handleFilterChange('cuisines', option)}
                  />
                  <span className="label-text">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Service Type */}
          <div className="filter-group">
            <h3>🚗 Service Type</h3>
            <div className="filter-options">
              {serviceTypes.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.serviceType.includes(option)}
                    onChange={() => handleFilterChange('serviceType', option)}
                  />
                  <span className="label-text">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Accessibility */}
          <div className="filter-group">
            <h3>♿ Accessibility</h3>
            <div className="filter-options">
              {accessibilityOptions.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.accessibility.includes(option)}
                    onChange={() => handleFilterChange('accessibility', option)}
                  />
                  <span className="label-text">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Operational */}
          <div className="filter-group">
            <h3>🕐 When to Eat</h3>
            <div className="filter-options">
              {operationalOptions.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="checkbox"
                    checked={filters.operational.includes(option)}
                    onChange={() => handleFilterChange('operational', option)}
                  />
                  <span className="label-text">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Minimum Rating */}
          <div className="filter-group">
            <h3>⭐ Minimum Rating</h3>
            <div className="filter-options rating-options">
              {ratingOptions.map(option => (
                <label key={option} className="filter-label">
                  <input
                    type="radio"
                    name="rating"
                    value={option}
                    checked={filters.minRating === option}
                    onChange={() => handleRatingChange(option)}
                  />
                  <span className="label-text">{option}+ Stars</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="filter-actions">
          <button className="reset-button" onClick={handleReset}>
            ↻ Reset All
          </button>
          <button className="apply-button" onClick={handleApply}>
            🔍 Search ({activeFilterCount} filters)
          </button>
        </div>
      </div>
    </div>
  );
}

export default FilterOverlay;
