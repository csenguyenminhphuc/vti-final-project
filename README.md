# Hệ Thống Quản Lý Sinh Viên - Triển Khai Docker Swarm

Dự án này triển khai một hệ thống quản lý sinh viên sử dụng Flask, PostgreSQL và Docker Swarm với 2 bản sao (replication).

## 👨‍💻 Thông Tin Nhà Phát Triển

- **Tên:** Nguyễn Minh Phúc
- **Nghề nghiệp:** Sinh viên năm 4 ngành Khoa học Máy tính  
- **Chuyên môn:** DevSecOps

## 🏗️ Kiến Trúc Hệ Thống

### Các Thành Phần Chính:
- **Frontend:** HTML và CSS thuần túy
- **Backend:** Python Flask với API REST
- **Cơ sở dữ liệu:** PostgreSQL
- **Load Balancer:** Nginx
- **Điều phối:** Docker Swarm
- **Kho lưu trữ Image:** Docker Hub

### Tính Năng:
1. **Trang chủ** - Giới thiệu cá nhân
2. **Hệ thống xác thực** - Đăng nhập để truy cập quản trị
3. **Quản lý sinh viên:**
   - Xem danh sách sinh viên
   - Thêm sinh viên mới
   - Chỉnh sửa thông tin sinh viên
   - Xóa sinh viên

### Trường Dữ Liệu Sinh Viên:
- Mã Sinh Viên (ID duy nhất)
- Họ và tên đầy đủ
- Tuổi
- Ngành học/Chuyên ngành
- Năm nhập học
- GPA (Điểm trung bình)

## 🚀 Hướng Dẫn Triển Khai

### Điều Kiện Tiên Quyết:
- Docker Engine 20.10+
- Docker Compose 2.0+
- Tài khoản Docker Hub
- Hệ điều hành Linux/Ubuntu

### 1. Chuẩn Bị Môi Trường

```bash
# Clone hoặc tải xuống các file của dự án
git clone https://github.com/csenguyenminhphuc/vti-final-project.git
cd vti-final-project

# Tạo file .env từ mẫu (nếu chưa có)
cp .env.example .env
```

### 2. Tạo và Cấu Hình File .env

Tạo file `.env` trong thư mục gốc của dự án với nội dung sau:

```env
# Cấu hình Cơ sở dữ liệu
DB_HOST=database
DB_NAME=students_db
DB_USER=postgres
DB_PASSWORD=MatKhauBaoMat123!
DB_PORT=5432

# Khóa bí mật Flask (QUAN TRỌNG: Thay đổi trong môi trường production)
SECRET_KEY=khoa-bi-mat-cuc-ky-bao-mat-thay-doi-trong-production-2024
FLASK_ENV=production

# Thông tin đăng nhập Admin (QUAN TRỌNG: Thay đổi trong môi trường production)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Cấu hình Docker Hub (thay đổi thành thông tin của bạn)
DOCKER_HUB_USERNAME=csenguyenminhphuc
DOCKER_HUB_TOKEN=your_docker_hub_token_here
IMAGE_NAME=student-management-system

# Cấu hình Stack
STACK_NAME=student-management
REPLICAS=2
PORT=5000
WORKERS=4

# Cấu hình Cloudflare (tùy chọn - để trống nếu không sử dụng)
API_TOKEN=your_cloudflare_api_token
ZONE_ID=your_cloudflare_zone_id
RECORD_ID=your_cloudflare_record_id
SUBDOMAIN=your-subdomain.your-domain.com
PRIMARY_IP=your_primary_server_ip
BACKUP_IP=your_backup_server_ip
```

**⚠️ LƯU Ý QUAN TRỌNG:** 
- Thay đổi tất cả các mật khẩu mặc định trước khi triển khai production
- Tạo Docker Hub token tại: https://hub.docker.com/settings/security
- Đảm bảo file `.env` không được commit vào Git (thêm vào `.gitignore`)

### 3. Phát Triển Cục Bộ

Để chạy thử nghiệm trên máy local với Docker Compose:

```bash
# Khởi động môi trường phát triển
docker-compose up -d

# Kiểm tra trạng thái các container
docker-compose ps

# Xem logs
docker-compose logs -f

# Dừng môi trường phát triển
docker-compose down
```

Truy cập ứng dụng tại: http://localhost

### 4. Build và Push Images

Trước khi triển khai Docker Swarm, bạn cần build và push images:

```bash
# Build image ứng dụng
docker build -t $DOCKER_HUB_USERNAME/student-management-app:latest .

# Build image database
docker build -f Dockerfile.db -t $DOCKER_HUB_USERNAME/student-management-db:latest .

# Build image nginx
docker build -f Dockerfile.nginx -t $DOCKER_HUB_USERNAME/student-management-nginx:latest .

# Đăng nhập Docker Hub
docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_TOKEN

# Push images lên Docker Hub
docker push $DOCKER_HUB_USERNAME/student-management-app:latest
docker push $DOCKER_HUB_USERNAME/student-management-db:latest
docker push $DOCKER_HUB_USERNAME/student-management-nginx:latest
```

### 5. Triển Khai với Docker Swarm

```bash
# Khởi tạo Docker Swarm (nếu chưa có)
docker swarm init

# Triển khai stack
docker stack deploy -c docker-stack.yml student-management

# Kiểm tra trạng thái các service
docker service ls

# Xem chi tiết stack
docker stack ps student-management
```

## 🔧 Cấu Trúc Dự Án

```
├── app.py                     # Ứng dụng Flask chính
├── python.py                  # File Python phụ trợ
├── requirements.txt           # Các thư viện Python cần thiết
├── templates/                 # Các template HTML
│   ├── base.html             # Template cơ sở
│   ├── home.html             # Trang chủ
│   ├── login.html            # Trang đăng nhập
│   └── dashboard.html        # Dashboard quản lý
├── static/                   # Tài nguyên tĩnh
│   └── css/
│       └── style.css         # File CSS chính
├── Dockerfile                # Dockerfile cho ứng dụng
├── Dockerfile.db             # Dockerfile cho PostgreSQL
├── Dockerfile.nginx          # Dockerfile cho Nginx
├── docker-compose.yml        # Cấu hình cho development
├── docker-stack.yml          # Cấu hình cho Docker Swarm
├── docker-stack-local.yml    # Cấu hình Swarm local
├── docker-stack-simple.yml   # Cấu hình Swarm đơn giản
├── docker-stack-fixed.yml    # Cấu hình Swarm đã sửa lỗi
├── nginx.conf                # Cấu hình Nginx
├── init-db.sql              # Scripts khởi tạo cơ sở dữ liệu
├── .env                     # Biến môi trường (tạo từ mẫu bên dưới)
├── huongdan.txt             # Hướng dẫn bằng tiếng Việt
└── README.md                # File hướng dẫn này
```

## 🌐 URL Truy Cập

### Môi Trường Phát Triển:
- **Ứng dụng chính:** http://localhost (qua Nginx)
- **Truy cập trực tiếp Flask:** http://localhost:5000
- **Cơ sở dữ liệu:** localhost:5432

### Môi Trường Production (Docker Swarm):
- **Ứng dụng chính:** http://localhost (qua Nginx Load Balancer)
- **Visualizer Swarm:** http://localhost:8080 (nếu được cấu hình)

## 🔐 Thông Tin Đăng Nhập Mặc Định

⚠️ **QUAN TRỌNG: Thay đổi trong môi trường production!**

```
Tên đăng nhập: admin
Mật khẩu: admin123
```

## 📊 Giám Sát và Quản Lý

### Các Lệnh Docker Swarm Hữu Ích:

```bash
# Xem trạng thái các service
docker service ls

# Xem chi tiết stack
docker stack ps student-management

# Xem logs của service
docker service logs student-management_webapp

# Tăng/giảm số lượng replica
docker service scale student-management_webapp=4

# Cập nhật service
docker service update student-management_webapp

# Xem các node trong Swarm
docker node ls

# Xóa toàn bộ stack
docker stack rm student-management
```

### Các Lệnh Debug:

```bash
# Chạy bash bên trong container
docker exec -it $(docker ps -q -f name=webapp) bash

# Xem logs real-time
docker service logs -f student-management_webapp

# Kiểm tra tình trạng service
docker service inspect student-management_webapp

# Xem tài nguyên sử dụng
docker stats

# Kiểm tra network
docker network ls
```

## 🛡️ Bảo Mật và Khuyến Nghị

### Cho Môi Trường Production:
1. **Thay đổi tất cả mật khẩu mặc định**
2. **Sử dụng HTTPS với chứng chỉ SSL**
3. **Cấu hình tường lửa phù hợp**
4. **Sử dụng Docker Swarm secrets cho thông tin nhạy cảm**
5. **Triển khai backup thường xuyên cho cơ sở dữ liệu**
6. **Giám sát logs và metrics**
7. **Cập nhật thường xuyên các image Docker**

### Triển Khai HTTPS:

```bash
# Tạo chứng chỉ SSL tự ký (chỉ cho development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx-selfsigned.key \
    -out nginx-selfsigned.crt \
    -subj "/C=VN/ST=HCM/L=HoChiMinh/O=Organization/CN=localhost"

# Cập nhật nginx.conf để sử dụng SSL
# Thêm chứng chỉ vào container Nginx
```

## 🔄 Quy Trình CI/CD Đề Xuất

```yaml
# Ví dụ GitHub Actions workflow
name: Deploy to Production
on:
  push:
    branches: [main]
  
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/student-management-app:${{ github.sha }} .
          docker push ${{ secrets.DOCKER_USERNAME }}/student-management-app:${{ github.sha }}
      
      - name: Deploy to Docker Swarm
        run: |
          docker stack deploy -c docker-stack.yml student-management
```

## 📈 Mở Rộng Hệ Thống

### Mở Rộng Theo Chiều Ngang:
```bash
# Tăng số replica của ứng dụng
docker service scale student-management_webapp=5

# Thêm node vào Swarm cluster
docker swarm join --token <token> <manager-ip>:2377
```

### Mở Rộng Theo Chiều Dọc:
- Tăng tài nguyên CPU/Memory trong file cấu hình
- Cập nhật giới hạn tài nguyên trong docker-stack.yml

## 🚨 Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp:

1. **Service không khởi động được:**
   ```bash
   # Kiểm tra logs chi tiết
   docker service logs student-management_webapp
   
   # Kiểm tra trạng thái service
   docker service ps student-management_webapp --no-trunc
   ```

2. **Không kết nối được cơ sở dữ liệu:**
   - Kiểm tra thông tin trong file `.env`
   - Đảm bảo service database đang chạy
   - Kiểm tra network connectivity

3. **Không tìm thấy Docker images:**
   - Đảm bảo images đã được push lên Docker Hub
   - Kiểm tra thông tin đăng nhập Docker Hub
   - Verify image tags trong docker-stack.yml

4. **Cổng đang được sử dụng:**
   - Dừng các service khác sử dụng cùng cổng
   - Thay đổi cổng trong file cấu hình

5. **Lỗi permission denied:**
   ```bash
   # Cấp quyền thực thi cho scripts
   chmod +x *.sh
   
   # Kiểm tra quyền Docker
   sudo usermod -aG docker $USER
   newgrp docker
   ```

## 🔧 Kiểm Tra Hệ Thống

### Health Check:
```bash
# Kiểm tra tình trạng containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Test kết nối database
docker exec -it $(docker ps -q -f name=database) psql -U postgres -d students_db -c "SELECT version();"

# Test ứng dụng web
curl -f http://localhost/ || echo "Web app không phản hồi"

# Kiểm tra sử dụng tài nguyên
docker system df
```

## 📞 Hỗ Trợ và Liên Hệ

Khi gặp vấn đề:
1. Kiểm tra logs của các service
2. Tham khảo tài liệu Docker Swarm
3. Kiểm tra issues trên repository GitHub

## 🎯 Roadmap Phát Triển

- [ ] Thêm tính năng import/export dữ liệu
- [ ] Triển khai monitoring với Prometheus/Grafana
- [ ] Thêm unit tests và integration tests
- [ ] Cải thiện UI/UX với framework hiện đại
- [ ] Thêm API documentation với Swagger
- [ ] Triển khai multi-environment (dev, staging, prod)

## 📄 Giấy Phép

Dự án này được tạo ra cho mục đích giáo dục và demo DevSecOps với Docker Swarm.

---
**Phát triển bởi Nguyễn Minh Phúc** - Sinh viên Khoa học Máy tính chuyên về DevSecOps
