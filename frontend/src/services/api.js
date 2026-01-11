import axios from 'axios';
import { API_BASE_URL } from '../config';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// API functions
export const queryAPI = {
  // Send natural language query and get SQL results
  submitQuery: async (query, userId) => {
    try {
      const response = await api.post('/answer', { 
        query,
        user_id: userId
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Get query history - filter by user_id
  getHistory: async (userId) => {
    try {
      const response = await api.get(`/history/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },
};

export default api;
