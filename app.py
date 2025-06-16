from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    if not os.path.exists('students.db'):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            major TEXT NOT NULL,
            gpa REAL NOT NULL
        )
        ''')
        
        # Insert sample data
        students = [
            ('john_doe', 'password123', 'John Doe', 'john@university.edu', 'Computer Science', 3.8),
            ('jane_smith', 'securepass', 'Jane Smith', 'jane@university.edu', 'Biology', 3.9),
            ('bob_johnson', 'bobpass', 'Bob Johnson', 'bob@university.edu', 'Mathematics', 3.5),
            ('admin', 'admin', 'Admin User', 'admin@university.edu', 'Administration', 4.0)
        ]
        
        cursor.executemany('''
        INSERT INTO students (username, password, name, email, major, gpa)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', students)
        
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # VULNERABLE TO SQL INJECTION - concatenating user input directly into query
    query = f"SELECT * FROM students WHERE username = '{username}' AND password = '{password}'"
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        student = cursor.fetchone()
        
        if student:
            # Convert row to dictionary
            student_data = {
                'id': student[0],
                'username': student[1],
                'name': student[3],
                'email': student[4],
                'major': student[5],
                'gpa': student[6]
            }
            return jsonify({'student': student_data})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)