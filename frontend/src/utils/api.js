import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const searchRestaurants = async (location, filters) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/restaurants/search`, {
      location,
      filters,
    });
    return response.data;
  } catch (error) {
    console.error('Error searching restaurants:', error);
    throw error;
  }
};

export const getRestaurantDetails = async (restaurantId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/restaurants/${restaurantId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching restaurant details:', error);
    throw error;
  }
};

export default {
  searchRestaurants,
  getRestaurantDetails,
};
