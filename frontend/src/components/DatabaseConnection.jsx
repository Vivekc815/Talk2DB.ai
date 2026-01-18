import React, { useState } from 'react';
import { queryAPI } from '../services/api';
import './DatabaseConnection.css';

const DatabaseConnection = ({ userId, onConnectionSuccess }) => {
  const [connectionName, setConnectionName] = useState('');
  const [dbType, setDbType] = useState('postgresql');
  const [connectionString, setConnectionString] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const handleConnect = async () => {
    if (!connectionName || !connectionString) {
      setError('Please provide connection name and connection string');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await queryAPI.connectDatabase(
        userId,
        connectionName,
        dbType,
        connectionString
      );

      if (response.success) {
        setSuccess(`Database "${connectionName}" connected successfully!`);
        setConnectionName('');
        setConnectionString('');
        setShowForm(false);
        
        if (onConnectionSuccess) {
          onConnectionSuccess(response);
        }
      } else {
        setError(response.error || 'Connection failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to database');
    } finally {
      setLoading(false);
    }
  };

  const exampleConnections = {
    postgresql: 'postgresql://username:password@hostname:5432/database_name',
    mysql: 'mysql+pymysql://username:password@hostname:3306/database_name',
    sqlite: '/path/to/database.db'
  };

  return (
    <div className="database-connection-container">
      <div className="connection-header">
        <h3>🔌 Connect Database</h3>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="toggle-button"
        >
          {showForm ? '−' : '+'}
        </button>
      </div>

      {showForm && (
        <div className="connection-form">
          <p className="connection-description">
            Connect to your PostgreSQL, MySQL, or SQLite database to extract schema
          </p>

          <div className="form-group">
            <label htmlFor="connectionName">Connection Name:</label>
            <input
              id="connectionName"
              type="text"
              value={connectionName}
              onChange={(e) => setConnectionName(e.target.value)}
              placeholder="e.g., My Production DB"
              className="connection-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="dbType">Database Type:</label>
            <select
              id="dbType"
              value={dbType}
              onChange={(e) => setDbType(e.target.value)}
              className="connection-input"
            >
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="sqlite">SQLite</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="connectionString">Connection String:</label>
            <textarea
              id="connectionString"
              value={connectionString}
              onChange={(e) => setConnectionString(e.target.value)}
              placeholder={exampleConnections[dbType]}
              className="connection-textarea"
              rows={3}
            />
            <div className="connection-hint">
              💡 Example: {exampleConnections[dbType]}
            </div>
          </div>

          <button
            onClick={handleConnect}
            disabled={loading || !connectionName || !connectionString}
            className="connect-button"
          >
            {loading ? 'Connecting...' : '🔗 Connect & Extract Schema'}
          </button>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          {success && (
            <div className="success-message">
              ✅ {success}
            </div>
          )}

          <div className="connection-note">
            <strong>Note:</strong> Connection strings are not stored. You'll need to provide it again for each query session.
          </div>
        </div>
      )}
    </div>
  );
};

export default DatabaseConnection;
