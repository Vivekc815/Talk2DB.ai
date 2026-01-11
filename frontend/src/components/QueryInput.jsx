import React, { useState } from 'react';
import './QueryInput.css';

const QueryInput = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
      setQuery('');
    }
  };

  return (
    <div className="query-input-container">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-wrapper">
          <div className="input-label">
            <span className="label-icon">💬</span>
            <span>Type your question here</span>
          </div>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Example: Show me all students with GPA above 3.5"
            className="query-textarea"
            rows={4}
            disabled={isLoading}
          />
          <div className="input-hint">
            💡 Tip: Be specific! The more details you provide, the better the SQL query will be.
          </div>
        </div>
        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? (
            <>
              <span className="button-spinner"></span>
              Processing...
            </>
          ) : (
            <>
              <span className="button-icon">🚀</span>
              Convert to SQL
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default QueryInput;
