// API Configuration - Environment-based
const getApiBaseUrl = () => {
  // Check if we have environment variable (production)
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  // Default to localhost for development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
