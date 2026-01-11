import React from 'react';
import './QueryResults.css';

const QueryResults = ({ data, error, isLoading }) => {
  if (isLoading) {
    return (
      <div className="results-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Processing your query...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="results-container empty-state">
        <div className="empty-content">
          <div className="empty-icon">💡</div>
          <h3>Ready to Learn SQL?</h3>
          <p>Ask a question above to see how natural language translates to SQL queries!</p>
          <div className="example-queries">
            <p className="examples-title">Try these examples:</p>
            <ul>
              <li>"Show me all students"</li>
              <li>"What are the computer science courses?"</li>
              <li>"List students with GPA above 3.5"</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="results-container">
      {/* Educational SQL Explanation */}
      <div className="sql-explanation-section">
        <div className="explanation-header">
          <h3>📚 How Your Question Became SQL</h3>
        </div>
        
        <div className="explanation-content">
          <div className="step-box">
            <div className="step-number">1</div>
            <div className="step-content">
              <h4>Your Question:</h4>
              <p className="user-question">"{data.query}"</p>
            </div>
          </div>

          <div className="arrow">↓</div>

          <div className="step-box">
            <div className="step-number">2</div>
            <div className="step-content">
              <h4>Generated SQL:</h4>
              <pre className="sql-code">{data.sql}</pre>
              <p className="sql-explanation">
                This SQL query retrieves data from the database. The SELECT statement specifies which columns to return, 
                FROM indicates the table, and WHERE filters the results (if applicable).
              </p>
            </div>
          </div>
        </div>

        {!data.is_safe && (
          <div className="error-section">
            <h4>⚠️ Safety Check Failed:</h4>
            <p className="error-text">{data.error}</p>
            <p className="error-explanation">
              The query was blocked for security reasons. Try rephrasing your question.
            </p>
          </div>
        )}
      </div>

      {/* Results Table - Directly below */}
      {data.is_safe && data.results && (
        <div className="results-section">
          <div className="results-header">
            <h3>📊 Query Results</h3>
            <p className="results-count">
              {data.results.length === 0 
                ? 'No rows found' 
                : `${data.results.length} row${data.results.length !== 1 ? 's' : ''} returned`
              }
            </p>
          </div>

          {data.results.length === 0 ? (
            <div className="no-results">
              <p>No results found for your query.</p>
              <p className="hint">Try modifying your question or check the database schema.</p>
            </div>
          ) : (
            <div className="table-container">
              <div className="table-wrapper">
                <table className="results-table">
                  <thead>
                    <tr>
                      {Object.keys(data.results[0]).map((key) => (
                        <th key={key}>
                          <span className="column-name">{key}</span>
                          <span className="column-type-hint">({getColumnType(data.results, key)})</span>
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.results.map((row, index) => (
                      <tr key={index}>
                        {Object.keys(data.results[0]).map((key) => (
                          <td key={key}>
                            {row[key] === null || row[key] === undefined ? (
                              <span className="null-value">NULL</span>
                            ) : (
                              <span>{String(row[key])}</span>
                            )}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="table-footer">
                <p className="learning-tip">
                  💡 <strong>Learning Tip:</strong> Each column represents an attribute, and each row represents a record. 
                  This is how relational databases store and organize data!
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Helper function to infer column type
const getColumnType = (results, columnName) => {
  if (results.length === 0) return 'unknown';
  const firstValue = results[0][columnName];
  if (firstValue === null || firstValue === undefined) return 'unknown';
  
  const value = String(firstValue);
  if (!isNaN(value) && value.trim() !== '') {
    return value.includes('.') ? 'decimal' : 'integer';
  }
  return 'text';
};

export default QueryResults;
