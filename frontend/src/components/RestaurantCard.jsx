import React, { useState, useEffect } from 'react';
import '../styles/RestaurantCard.css';

function RestaurantCard({ restaurant, style }) {
  const [imageError, setImageError] = useState(false);
  
  // Only use REAL restaurant images - show placeholder if no real image available
  const getImageUrl = () => {
    // Only use if it's a real restaurant image (not generic placeholder or example URL)
    if (restaurant.image && 
        restaurant.image.startsWith('http') && 
        !restaurant.image.includes('picsum') && 
        !restaurant.image.includes('unsplash') &&
        !restaurant.image.includes('placeholder') &&
        !restaurant.image.includes('example.com') &&
        !restaurant.image.includes('example.org') &&
        !restaurant.image.includes('lorem') &&
        !restaurant.image.includes('dummy')) {
      return restaurant.image;
    }
    // Return null if no real image (will show placeholder SVG)
    return null;
  };

  const imageSrc = getImageUrl();

  // Placeholder for when no real restaurant image is available
  const defaultPlaceholder = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23e8e8e8;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23d0d0d0;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23grad)' width='400' height='300'/%3E%3Ctext fill='%23888' font-family='Arial, sans-serif' font-size='48' font-weight='normal' x='200' y='130' text-anchor='middle' dominant-baseline='middle'%3E🍽️%3C/text%3E%3Ctext fill='%23666' font-family='Arial, sans-serif' font-size='14' x='200' y='170' text-anchor='middle' dominant-baseline='middle'%3ERestaurant Image%3C/text%3E%3Ctext fill='%23999' font-family='Arial, sans-serif' font-size='12' x='200' y='190' text-anchor='middle' dominant-baseline='middle'%3ENot Available%3C/text%3E%3C/svg%3E";
  
  // Final image source - use real image or placeholder
  const finalImageSrc = imageSrc || defaultPlaceholder;
  
  // Update error state when image fails
  const handleImageError = () => {
    console.log(`Real restaurant image failed to load for ${restaurant.name}:`, imageSrc);
    setImageError(true);
  };

  // Log image URL for debugging
  useEffect(() => {
    if (restaurant.image && imageSrc) {
      console.log(`✅ Restaurant: ${restaurant.name}, Image URL: ${restaurant.image}`);
    } else if (!restaurant.image) {
      console.warn(`⚠️ Restaurant: ${restaurant.name} has no image available (will show placeholder)`);
    }
  }, [restaurant.name, restaurant.image, imageSrc]);

  return (
    <div className="restaurant-card" style={style}>
      <div className="card-image">
        <img 
          src={finalImageSrc}
          alt={restaurant.name}
          onError={handleImageError}
          loading="lazy"
          key={`${restaurant.name}-${imageSrc || 'placeholder'}`} // Force re-render when image changes
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
              📋 View Full Menu
            </a>
          )}
          {restaurant.website && (
            <a href={restaurant.website} target="_blank" rel="noopener noreferrer" className="website-link">
              🌐 Visit Website
            </a>
          )}
        </div>

        {(restaurant.website || restaurant.menuLink) && (
          <div className="card-links">
            {restaurant.website && (
              <p className="link-info">
                Website: <a href={restaurant.website} target="_blank" rel="noopener noreferrer">{restaurant.website}</a>
              </p>
            )}
            {restaurant.menuLink && (
              <p className="link-info">
                Menu: <a href={restaurant.menuLink} target="_blank" rel="noopener noreferrer">{restaurant.menuLink}</a>
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default RestaurantCard;
