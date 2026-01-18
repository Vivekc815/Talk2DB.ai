import React, { useState, useEffect, useCallback } from 'react';
import { queryAPI } from '../services/api';
import './SchemaManager.css';

const SchemaManager = ({ userId, onSchemaSelect }) => {
  const [schemas, setSchemas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSchemaId, setSelectedSchemaId] = useState(null);

  const loadSchemas = useCallback(async () => {
    if (!userId) return;
    
    try {
      setLoading(true);
      const response = await queryAPI.getSchemas(userId);
      if (response.success) {
        setSchemas(response.schemas || []);
      }
    } catch (err) {
      console.error('Error loading schemas:', err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    loadSchemas();
  }, [loadSchemas]);

  const handleSchemaSelect = (schemaId) => {
    setSelectedSchemaId(schemaId);
    if (onSchemaSelect) {
      onSchemaSelect(schemaId);
    }
  };

  const handleDeleteSchema = async (schemaId) => {
    try {
      const response = await queryAPI.deleteSchema(userId, schemaId);
      if (response.success) {
        loadSchemas();
        if (selectedSchemaId === schemaId) {
          setSelectedSchemaId(null);
          if (onSchemaSelect) {
            onSchemaSelect(null);
          }
        }
      }
    } catch (err) {
      console.error('Error deleting schema:', err);
    }
  };

  if (loading) {
    return (
      <div className="schema-manager">
        <h3>📚 Your Schemas</h3>
        <p>Loading schemas...</p>
      </div>
    );
  }

  return (
    <div className="schema-manager">
      <div className="schema-header">
        <h3>📚 Your Schemas</h3>
        <button onClick={loadSchemas} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {schemas.length === 0 ? (
        <p className="no-schemas">
          No schemas yet. Upload a SQL or CSV file to create one.
        </p>
      ) : (
        <div className="schema-list">
          {schemas.map((schema) => (
            <div
              key={schema.id}
              className={`schema-item ${selectedSchemaId === schema.id ? 'selected' : ''}`}
              onClick={() => handleSchemaSelect(schema.id)}
            >
              <div className="schema-item-header">
                <div>
                  <h4>{schema.schema_name}</h4>
                  <span className="schema-type-badge">{schema.schema_type}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteSchema(schema.id);
                  }}
                  className="delete-button"
                  title="Delete schema"
                >
                  ✕
                </button>
              </div>
              <p className="schema-info">
                {schema.tables.length} table{schema.tables.length !== 1 ? 's' : ''}
                {schema.file_name && ` • ${schema.file_name}`}
              </p>
            </div>
          ))}
        </div>
      )}

      {selectedSchemaId && (
        <div className="selected-schema-indicator">
          ✓ Using schema: {schemas.find(s => s.id === selectedSchemaId)?.schema_name}
        </div>
      )}
    </div>
  );
};

export default SchemaManager;
