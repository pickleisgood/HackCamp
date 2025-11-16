import React, { useState } from 'react';
import '../styles/RestaurantCard.css';

function RestaurantCard({ restaurant }) {
  const [imageError, setImageError] = useState(false);

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className="restaurant-card">
      <div className="card-image">
        <img 
          src={imageError ? 'https://via.placeholder.com/400x300?text=No+Image' : (restaurant.image || 'https://via.placeholder.com/400x300')} 
          alt={restaurant.name}
          onError={handleImageError}
          loading="lazy"
        />
      </div>

      <div className="card-content">
        <h3>{restaurant.name}</h3>
        
        <div className="rating">
          <span className="stars">⭐ {restaurant.rating || 'N/A'}</span>
        </div>

        <p className="address">{restaurant.address}</p>

        {restaurant.phone && (
          <p className="phone">📞 {restaurant.phone}</p>
        )}

        <div className="budget">
          <span className="budget-indicator">{restaurant.budget || 'N/A'}</span>
        </div>

        {restaurant.cuisines && restaurant.cuisines.length > 0 && (
          <div className="cuisines">
            <span className="cuisine-tag">{restaurant.cuisines.join(', ')}</span>
          </div>
        )}

        <div className="menu-items">
          <h4>Menu Items (Matching Dietary Restrictions)</h4>
          <ul>
            {restaurant.matchingItems?.map((item, idx) => (
              <li key={idx}>{item}</li>
            )) || <li>No items available</li>}
          </ul>
        </div>

        <div className="card-actions">
          {restaurant.menuLink && (
            <a href={restaurant.menuLink} target="_blank" rel="noopener noreferrer" className="menu-link">
              View Full Menu
            </a>
          )}
          {restaurant.website && (
            <a href={restaurant.website} target="_blank" rel="noopener noreferrer" className="website-link">
              Visit Website
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

export default RestaurantCard;
