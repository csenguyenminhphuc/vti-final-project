-- Initialize the students database with proper schema
-- Note: Database is already created by Docker environment variables
-- \c students_db;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 16 AND age <= 50),
    major VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    gpa DECIMAL(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_students_student_id ON students(student_id);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(course);
CREATE INDEX IF NOT EXISTS idx_students_major ON students(major);

-- Insert sample data
INSERT INTO students (student_id, full_name, age, major, course, gpa) VALUES
('SV001', 'Nguyễn Văn An', 20, 'Khoa học Máy tính', 'K2021', 3.5),
('SV002', 'Trần Thị Bình', 21, 'Công nghệ Thông tin', 'K2020', 3.8),
('SV003', 'Lê Văn Cường', 19, 'Khoa học Máy tính', 'K2022', 3.2),
('SV004', 'Phạm Thị Dung', 22, 'An toàn Thông tin', 'K2019', 3.9),
('SV005', 'Hoàng Văn Em', 20, 'Trí tuệ Nhân tạo', 'K2021', 3.6),
('SV006', 'Nguyễn Thị Flower', 21, 'Kỹ thuật Phần mềm', 'K2020', 3.7),
('SV007', 'Võ Văn Giang', 19, 'Khoa học Máy tính', 'K2022', 3.4),
('SV008', 'Đặng Thị Hồng', 20, 'An toàn Thông tin', 'K2021', 3.9),
('SV009', 'Bùi Văn Inh', 22, 'Trí tuệ Nhân tạo', 'K2019', 3.3),
('SV010', 'Cao Thị Kiều', 21, 'Công nghệ Thông tin', 'K2020', 3.6)
ON CONFLICT (student_id) DO NOTHING;

-- Create function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
CREATE TRIGGER update_students_updated_at 
    BEFORE UPDATE ON students 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();