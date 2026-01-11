import React, { useState } from 'react';
import './DatabaseSchema.css';

const DatabaseSchema = () => {
  const [activeTable, setActiveTable] = useState('students');

  const tables = {
    students: {
      name: 'students',
      description: 'Student information and academic records',
      columns: [
        { name: 'id', type: 'SERIAL', nullable: false, description: 'Primary key - unique identifier for each student' },
        { name: 'name', type: 'VARCHAR(100)', nullable: true, description: 'Student full name' },
        { name: 'age', type: 'INTEGER', nullable: true, description: 'Student age in years' },
        { name: 'email', type: 'VARCHAR(100)', nullable: true, description: 'Student email address' },
        { name: 'gpa', type: 'DECIMAL(3,2)', nullable: true, description: 'Grade Point Average (0.00 to 4.00)' },
        { name: 'major', type: 'VARCHAR(100)', nullable: true, description: 'Field of study (e.g., Computer Science, Mathematics)' },
        { name: 'enrollment_year', type: 'INTEGER', nullable: true, description: 'Year when student enrolled' },
        { name: 'created_at', type: 'TIMESTAMP', nullable: true, description: 'Record creation timestamp' },
      ]
    },
    courses: {
      name: 'courses',
      description: 'Course catalog information',
      columns: [
        { name: 'id', type: 'SERIAL', nullable: false, description: 'Primary key - unique identifier for each course' },
        { name: 'name', type: 'VARCHAR(100)', nullable: true, description: 'Full course name' },
        { name: 'code', type: 'VARCHAR(20)', nullable: true, description: 'Course code (e.g., CS101, MATH201)' },
        { name: 'credits', type: 'INTEGER', nullable: true, description: 'Number of credit hours (typically 1-4)' },
        { name: 'department', type: 'VARCHAR(100)', nullable: true, description: 'Department offering the course' },
        { name: 'created_at', type: 'TIMESTAMP', nullable: true, description: 'Record creation timestamp' },
      ]
    },
    teachers: {
      name: 'teachers',
      description: 'Teacher/faculty information',
      columns: [
        { name: 'id', type: 'SERIAL', nullable: false, description: 'Primary key - unique identifier for each teacher' },
        { name: 'name', type: 'VARCHAR(100)', nullable: true, description: 'Teacher full name' },
        { name: 'department', type: 'VARCHAR(100)', nullable: true, description: 'Department affiliation' },
        { name: 'email', type: 'VARCHAR(100)', nullable: true, description: 'Teacher email address' },
        { name: 'years_experience', type: 'INTEGER', nullable: true, description: 'Years of teaching experience' },
        { name: 'created_at', type: 'TIMESTAMP', nullable: true, description: 'Record creation timestamp' },
      ]
    }
  };

  const activeTableData = tables[activeTable];

  return (
    <div className="database-schema-container">
      <div className="schema-header">
        <h2>📚 Database Schema</h2>
        <p className="schema-subtitle">Learn the table structure to write better queries</p>
      </div>

      <div className="schema-content">
        <div className="table-selector">
          {Object.keys(tables).map((tableName) => (
            <button
              key={tableName}
              className={`table-tab ${activeTable === tableName ? 'active' : ''}`}
              onClick={() => setActiveTable(tableName)}
            >
              {tableName}
            </button>
          ))}
        </div>

        <div className="table-details">
          <div className="table-info">
            <h3 className="table-name">{activeTableData.name}</h3>
            <p className="table-description">{activeTableData.description}</p>
          </div>

          <div className="columns-table-wrapper">
            <table className="columns-table">
              <thead>
                <tr>
                  <th>Column Name</th>
                  <th>Data Type</th>
                  <th>Nullable</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {activeTableData.columns.map((column, index) => (
                  <tr key={index}>
                    <td className="column-name">
                      {column.name}
                      {column.name === 'id' && <span className="pk-badge">PK</span>}
                    </td>
                    <td className="column-type">
                      <code>{column.type}</code>
                    </td>
                    <td className="column-nullable">
                      {column.nullable ? (
                        <span className="nullable-yes">Yes</span>
                      ) : (
                        <span className="nullable-no">No</span>
                      )}
                    </td>
                    <td className="column-description">{column.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="example-query">
            <h4>💡 Try This Query:</h4>
            <pre className="example-sql">
              <code>{`SELECT * FROM ${activeTableData.name} LIMIT 5;`}</code>
            </pre>
            <p className="query-explanation">
              This query selects all columns (*) from the {activeTableData.name} table and limits the results to 5 rows.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatabaseSchema;
