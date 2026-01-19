// API Configuration - Environment-based
const getApiBaseUrl = () => {
  // Check if we have environment variable (production)
  if (process.env.REACT_APP_API_URL) {
    const url = process.env.REACT_APP_API_URL;
    console.log('Using API URL from environment:', url);
    return url;
  }
  
  // Check if we're in production (deployed)
  if (process.env.NODE_ENV === 'production') {
    // Try to detect backend URL from window location
    const hostname = window.location.hostname;
    // If on Render, backend is typically on a different subdomain or path
    // Common pattern: frontend on static site, backend on web service
    // You may need to set REACT_APP_API_URL in Render's environment variables
    console.warn('⚠️ Production mode detected but REACT_APP_API_URL not set!');
    console.warn('Please set REACT_APP_API_URL environment variable in Render');
    console.warn('Current hostname:', hostname);
  }
  
  // Default to localhost for development
  const devUrl = 'http://localhost:8000';
  console.log('Using default development API URL:', devUrl);
  return devUrl;
};

export const API_BASE_URL = getApiBaseUrl();

// Log the API URL being used (helpful for debugging)
console.log('🔗 API Base URL:', API_BASE_URL);
