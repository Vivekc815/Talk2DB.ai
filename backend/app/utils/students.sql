-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    email VARCHAR(100),
    gpa DECIMAL(3,2),
    major VARCHAR(100),
    enrollment_year INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create courses table
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    code VARCHAR(20),
    credits INTEGER,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create teachers table
CREATE TABLE IF NOT EXISTS teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100),
    years_experience INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert students
INSERT INTO students (name, age, email, gpa, major, enrollment_year) VALUES
    ('Alice Johnson', 20, 'alice@school.com', 3.85, 'Computer Science', 2022),
    ('Bob Smith', 19, 'bob@school.com', 3.42, 'Computer Science', 2023),
    ('Charlie Brown', 21, 'charlie@school.com', 3.91, 'Computer Science', 2021),
    ('Diana Prince', 20, 'diana@school.com', 3.67, 'Mathematics', 2022),
    ('Eve Davis', 19, 'eve@school.com', 2.95, 'Computer Science', 2023),
    ('Frank Miller', 22, 'frank@school.com', 3.78, 'Computer Science', 2020),
    ('Grace Lee', 20, 'grace@school.com', 3.55, 'Mathematics', 2022),
    ('Henry Wilson', 19, 'henry@school.com', 3.21, 'Computer Science', 2023),
    ('Ivy Chen', 21, 'ivy@school.com', 3.95, 'Computer Science', 2021),
    ('Jack Robinson', 20, 'jack@school.com', 3.48, 'Mathematics', 2022);

-- Insert courses
INSERT INTO courses (name, code, credits, department) VALUES
    ('Introduction to Programming', 'CS101', 4, 'Computer Science'),
    ('Data Structures', 'CS201', 4, 'Computer Science'),
    ('Database Systems', 'CS301', 3, 'Computer Science'),
    ('Machine Learning', 'CS401', 4, 'Computer Science'),
    ('Web Development', 'CS202', 3, 'Computer Science'),
    ('Linear Algebra', 'MATH201', 3, 'Mathematics'),
    ('Calculus II', 'MATH102', 4, 'Mathematics');

-- Insert teachers
INSERT INTO teachers (name, department, email, years_experience) VALUES
    ('Dr. Sarah Smith', 'Computer Science', 'sarah@school.com', 15),
    ('Prof. Michael Johnson', 'Computer Science', 'michael@school.com', 12),
    ('Dr. Emily Williams', 'Mathematics', 'emily@school.com', 18);

-- Verify
SELECT 'Students:' as table_name, COUNT(*) as count FROM students
UNION ALL
SELECT 'Courses:' as table_name, COUNT(*) as count FROM courses
UNION ALL
SELECT 'Teachers:' as table_name, COUNT(*) as count FROM teachers
UNION ALL
SELECT 'Query History:' as table_name, COUNT(*) as count FROM "NLPtoSQL";