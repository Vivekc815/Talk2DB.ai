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
  submitQuery: async (query, userId, schemaId = null) => {
    try {
      const response = await api.post('/answer', { 
        query,
        user_id: userId,
        schema_id: schemaId
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

  // Upload SQL file
  uploadSQLFile: async (userId, schemaName, file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId);
      formData.append('schema_name', schemaName);

      const response = await api.post('/upload/sql', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 seconds for file upload
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Upload CSV file
  uploadCSVFile: async (userId, schemaName, file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId);
      formData.append('schema_name', schemaName);

      const response = await api.post('/upload/csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 seconds for file upload
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Upload PDF file
  uploadPDFFile: async (userId, schemaName, file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', userId);
      formData.append('schema_name', schemaName);

      const response = await api.post('/upload/pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 120000, // 120 seconds for PDF processing (AI takes time)
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Query connected database
  queryConnectedDatabase: async (userId, query, dbType, connectionString) => {
    try {
      const response = await api.post('/query/database', {
        user_id: userId,
        query: query,
        db_type: dbType,
        connection_string: connectionString
      }, {
        timeout: 60000, // 60 seconds
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Connect to external database
  connectDatabase: async (userId, schemaName, dbType, connectionString) => {
    try {
      const response = await api.post('/connect/database', {
        user_id: userId,
        schema_name: schemaName,
        db_type: dbType,
        connection_string: connectionString
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Get all schemas for a user
  getSchemas: async (userId) => {
    try {
      const response = await api.get(`/schemas/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Get schema details
  getSchemaDetails: async (userId, schemaId) => {
    try {
      const response = await api.get(`/schemas/${userId}/${schemaId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },

  // Delete schema
  deleteSchema: async (userId, schemaId) => {
    try {
      const response = await api.delete(`/schemas/${userId}/${schemaId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: error.message };
    }
  },
};

export default api;
