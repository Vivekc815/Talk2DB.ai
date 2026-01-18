import React, { useState } from 'react';
import { queryAPI } from './services/api';
import QueryInput from './components/QueryInput';
import QueryResults from './components/QueryResults';
import DatabaseSchema from './components/DatabaseSchema';
import FileUpload from './components/FileUpload';
import DatabaseConnection from './components/DatabaseConnection';
import SchemaManager from './components/SchemaManager';
import History from './components/History';
import './App.css';

function App() {
  const [queryData, setQueryData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedSchemaId, setSelectedSchemaId] = useState(null);
  
  // Initialize user_id from localStorage or generate new one
  const [userId, setUserId] = useState(() => {
    const stored = localStorage.getItem('talk2db_user_id');
    if (stored) {
      return parseInt(stored, 10);
    }
    // Generate a random user ID if none exists
    const newUserId = Math.floor(Math.random() * 1000000);
    localStorage.setItem('talk2db_user_id', newUserId.toString());
    return newUserId;
  });

  const handleQuerySubmit = async (query) => {
    setIsLoading(true);
    setError(null);
    setQueryData(null);

    try {
      const response = await queryAPI.submitQuery(query, userId, selectedSchemaId);
      setQueryData(response);
    } catch (err) {
      setError(err.message || 'An error occurred while processing your query');
      console.error('Query error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUserIdChange = (newUserId) => {
    const userIdNum = parseInt(newUserId, 10);
    if (!isNaN(userIdNum) && userIdNum > 0) {
      setUserId(userIdNum);
      localStorage.setItem('talk2db_user_id', userIdNum.toString());
    }
  };

  const handleSchemaUploaded = (response) => {
    // Refresh schema list if needed
    console.log('Schema uploaded:', response);
    // You could reload schemas here
  };

  const handleSchemaSelect = (schemaId) => {
    setSelectedSchemaId(schemaId);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">🗣️</span>
            Talk2db<span className="ai-badge">.ai</span>
          </h1>
          <p className="subtitle">Learn SQL by asking questions in plain English</p>
        </div>
        <div className="user-info">
          <label htmlFor="userId">Student ID: </label>
          <input
            id="userId"
            type="number"
            value={userId}
            onChange={(e) => handleUserIdChange(e.target.value)}
            min="1"
            className="user-id-input"
          />
        </div>
      </header>

      <main className="app-main">
        <div className="main-content">
          {/* Sidebar */}
          <aside className="sidebar">
            <DatabaseSchema />
            
            {/* File Upload Section */}
            <FileUpload userId={userId} onSchemaUploaded={handleSchemaUploaded} />
            
            {/* Database Connection Section */}
            <DatabaseConnection userId={userId} onConnectionSuccess={handleSchemaUploaded} />
            
            {/* Schema Manager */}
            <SchemaManager userId={userId} onSchemaSelect={handleSchemaSelect} />
            
            <History userId={userId} />
          </aside>

          {/* Main Learning Area */}
          <div className="learning-area">
            <div className="query-section">
              <div className="section-header">
                <h2>📝 Ask Your Question</h2>
                <p className="section-description">Type your question in natural language and see how it translates to SQL</p>
                {selectedSchemaId && (
                  <div className="schema-indicator">
                    💡 Using uploaded schema for query generation
                  </div>
                )}
              </div>
              
              <QueryInput onSubmit={handleQuerySubmit} isLoading={isLoading} />
              
              {error && (
                <div className="error-message">
                  <strong>⚠️ Error:</strong> {error}
                </div>
              )}
            </div>

            {/* Results Section - Directly below query input */}
            <QueryResults 
              data={queryData} 
              error={error} 
              isLoading={isLoading} 
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
