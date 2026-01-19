import React, { useState } from 'react';
import { queryAPI } from '../services/api';
import './FileUpload.css';

const FileUpload = ({ userId, onSchemaUploaded }) => {
  const [file, setFile] = useState(null);
  const [schemaName, setSchemaName] = useState('');
  const [fileType, setFileType] = useState('sql');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const ext = selectedFile.name.split('.').pop().toLowerCase();
      setFileType(ext);
      
      // Auto-fill schema name
      if (!schemaName) {
        setSchemaName(selectedFile.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleUpload = async () => {
    if (!file || !schemaName) {
      setError('Please select a file and provide a schema name');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      let response;
      
      if (fileType === 'sql') {
        response = await queryAPI.uploadSQLFile(userId, schemaName, file);
      } else if (fileType === 'csv') {
        response = await queryAPI.uploadCSVFile(userId, schemaName, file);
      } else if (fileType === 'pdf') {
        response = await queryAPI.uploadPDFFile(userId, schemaName, file);
      } else {
        setError('Unsupported file type. Please upload .sql, .csv, or .pdf files');
        setLoading(false);
        return;
      }

      if (response.success) {
        setSuccess(`Schema "${schemaName}" uploaded successfully!`);
        setFile(null);
        setSchemaName('');
        if (onSchemaUploaded) {
          onSchemaUploaded(response);
        }
      } else {
        const errorMsg = response.error || 'Upload failed';
        setError(errorMsg);
        console.error('Upload error:', errorMsg);
      }
    } catch (err) {
      // Extract error message from various possible formats
      let errorMessage = 'Failed to upload file';
      
      // Handle different error formats
      if (err.error) {
        errorMessage = err.error;
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.response?.data?.message) {
        errorMessage = err.response.data.message;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      // Special handling for network errors
      if (errorMessage.toLowerCase().includes('network') || 
          errorMessage.toLowerCase().includes('timeout') ||
          errorMessage.toLowerCase().includes('connection')) {
        errorMessage = `🌐 ${errorMessage}\n\n💡 Tips:\n- Check your internet connection\n- Try a smaller PDF file (< 5MB)\n- Make sure the PDF contains readable text (not scanned images)\n- Wait a moment and try again`;
      }
      
      setError(errorMessage);
      console.error('Upload exception:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <h3>📁 Upload Schema File</h3>
      <p className="upload-description">
        Upload SQL, CSV, or PDF files to extract database schema
      </p>
      
      <div className="upload-form">
        <div className="form-group">
          <label htmlFor="schemaName">Schema Name:</label>
          <input
            id="schemaName"
            type="text"
            value={schemaName}
            onChange={(e) => setSchemaName(e.target.value)}
            placeholder="e.g., My Database Schema"
            className="schema-name-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="fileInput">Select File:</label>
          <input
            id="fileInput"
            type="file"
            accept=".sql,.csv,.pdf"
            onChange={handleFileChange}
            className="file-input"
          />
          {file && (
            <div className="file-info">
              📄 {file.name} ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}
        </div>

        <button
          onClick={handleUpload}
          disabled={loading || !file || !schemaName}
          className="upload-button"
        >
          {loading ? 'Uploading...' : '📤 Upload & Extract Schema'}
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
      </div>
    </div>
  );
};

export default FileUpload;
