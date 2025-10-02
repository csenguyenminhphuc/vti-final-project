from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from werkzeug.security import check_password_hash, generate_password_hash
import logging

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'students_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

# Admin credentials (in production, store these securely)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        app.logger.error(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Create students table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(20) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                major VARCHAR(100) NOT NULL,
                course VARCHAR(50) NOT NULL,
                gpa DECIMAL(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample data if table is empty
        cur.execute("SELECT COUNT(*) FROM students")
        if cur.fetchone()[0] == 0:
            sample_students = [
                ('SV001', 'Nguyễn Văn An', 20, 'Khoa học Máy tính', 'K2021', 3.5),
                ('SV002', 'Trần Thị Bình', 21, 'Công nghệ Thông tin', 'K2020', 3.8),
                ('SV003', 'Lê Văn Cường', 19, 'Khoa học Máy tính', 'K2022', 3.2),
                ('SV004', 'Phạm Thị Dung', 22, 'An toàn Thông tin', 'K2019', 3.9),
                ('SV005', 'Hoàng Văn Em', 20, 'Trí tuệ Nhân tạo', 'K2021', 3.6)
            ]
            
            for student in sample_students:
                cur.execute("""
                    INSERT INTO students (student_id, full_name, age, major, course, gpa)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, student)
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        app.logger.error(f"Database initialization error: {e}")
        return False

@app.route('/')
def home():
    """Home page with personal introduction"""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for admin access"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """Student management dashboard"""
    if not session.get('logged_in'):
        flash('Vui lòng đăng nhập để truy cập!', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    """API to get all students"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM students ORDER BY student_id")
        students = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([dict(student) for student in students])
    except psycopg2.Error as e:
        app.logger.error(f"Error fetching students: {e}")
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """API to add a new student"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    required_fields = ['student_id', 'full_name', 'age', 'major', 'course', 'gpa']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (student_id, full_name, age, major, course, gpa)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data['student_id'], data['full_name'], data['age'], 
              data['major'], data['course'], data['gpa']))
        
        student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Student added successfully', 'id': student_id}), 201
    except psycopg2.IntegrityError:
        return jsonify({'error': 'Student ID already exists'}), 400
    except psycopg2.Error as e:
        app.logger.error(f"Error adding student: {e}")
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """API to update a student"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE students SET 
            student_id = %s, full_name = %s, age = %s, 
            major = %s, course = %s, gpa = %s
            WHERE id = %s
        """, (data['student_id'], data['full_name'], data['age'],
              data['major'], data['course'], data['gpa'], student_id))
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Student not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Student updated successfully'})
    except psycopg2.Error as e:
        app.logger.error(f"Error updating student: {e}")
        return jsonify({'error': 'Database error'}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """API to delete a student"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Student not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Student deleted successfully'})
    except psycopg2.Error as e:
        app.logger.error(f"Error deleting student: {e}")
        return jsonify({'error': 'Database error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')