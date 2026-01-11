import React, { useState, useEffect, useCallback } from 'react';
import { queryAPI } from '../services/api';
import './History.css';

const History = ({ userId }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadHistory = useCallback(async () => {
    if (!userId) return;
    
    try {
      setLoading(true);
      const response = await queryAPI.getHistory(userId);
      setHistory(response.data || []);
      setError(null);
    } catch (err) {
      setError('Failed to load history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  if (loading) {
    return <div className="history-container">Loading history...</div>;
  }

  if (error) {
    return (
      <div className="history-container">
        <p className="error">{error}</p>
        <button onClick={loadHistory} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Query History</h2>
        <button onClick={loadHistory} className="refresh-button">
          Refresh
        </button>
      </div>
      
      {history.length === 0 ? (
        <p className="no-history">No query history yet.</p>
      ) : (
        <div className="history-list">
          {history.map((item) => (
            <div key={item.id} className="history-item">
              <div className="history-query">
                <strong>Query:</strong> {item.user_query}
              </div>
              <div className="history-sql">
                <strong>SQL:</strong>
                <pre>{item.generated_sql}</pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
