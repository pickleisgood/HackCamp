import React, { useState } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import RestaurantCard from './RestaurantCard';
import '../styles/RestaurantList.css';

function RestaurantList({ restaurants, loading }) {
  const [displayedCount, setDisplayedCount] = useState(10);

  const fetchMore = () => {
    setDisplayedCount(prev => prev + 10);
  };

  return (
    <div className="restaurant-list">
      <InfiniteScroll
        dataLength={Math.min(displayedCount, restaurants.length)}
        next={fetchMore}
        hasMore={displayedCount < restaurants.length}
        loader={<h4>Loading more restaurants...</h4>}
        endMessage={
          <p style={{ textAlign: 'center' }}>
            {restaurants.length === 0 
              ? 'No restaurants found. Try adjusting your filters.' 
              : 'No more restaurants to display.'}
          </p>
        }
      >
        {restaurants.slice(0, displayedCount).map((restaurant, index) => (
          <RestaurantCard key={index} restaurant={restaurant} />
        ))}
      </InfiniteScroll>
    </div>
  );
}

export default RestaurantList;
