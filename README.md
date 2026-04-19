# Hệ thống đặt lịch khám bệnh trực tuyến (Medical Appointment B3)

## 1. Mô tả dự án
Mục tiêu là hệ thống đặt lịch khám trực tuyến cho phòng khám hoặc bệnh viện: Bệnh nhân và lễ tân đặt lịch theo slot thời gian thông qua tìm kiếm bác sĩ, chuyên khoa và được xem hồ sơ bệnh nhân trong phạm vi nghiệp vụ. Bác sĩ quản lý lịch làm việc và hồ sơ người bệnh được phụ trách. Bên cạnh đó, hệ thống tự động thông báo và nhắc lịch hẹn và admin quản lý thông tin bác sĩ và chuyên khoa.

## 2. Thành viên nhóm

| MSSV | Họ và tên | Vai trò | Đảm nhiệm |
| :--- | :--- | :--- | :--- |
| **2351050164** | Văn Trung Thành | Nhóm trưởng | DevOps |
| **2351050133** | Nguyễn Thanh Phong | Thành viên | Backend |
| **2351010154** | Trương Hưng Phát | Thành viên | Frontend |

## 3. Công nghệ sử dụng

### Các công nghệ chính
| Container | Công nghệ | Phiên bản |
| :--- | :--- | :--- |
| **Backend** | Flask + Flask-RESTX | Flask >= 3.1.3, Flask-RESTX >= 1.3.2 |
| **Frontend** | React + Vite | React >= 19.2.4, Vite >= 7.3.1 |
| **Database** | MySQL debian | Mysql:8.0-debian |
| **Message Queue** | RabbitMQ | rabbitmq:4.0-management |
| **Cache** | Redis | Redis:7-alpine |

### Các công nghệ khác
- **Container:** Docker (v29.3.0) và Docker Compose (v5.1.0)
- **Version control:** Git (Latest) và GitHub

## 4. Kiến trúc hệ thống
Hệ thống được thiết kế dựa trên mẫu kiến trúc Client–Server với phong cách kiến trúc là REST. Bốn đặc tính được chọn là sự phù hợp chức năng, bảo mật, độ tin cậy và hiệu suất. 

Trong đó, hệ thống có 5 containers chính và hai containers phụ được định nghĩa và chạy lệnh qua docker-compose.yml. 

Tóm tắt luồng hoạt động:
Client-side (Browser) → API Server → Redis: lấy link cloudinary/payload ít thay đổi → MySQL: truy vấn dữ liệu nếu Redis không có cache. Ngoài ra, RabbitMQ xử lý bất đồng bộ giữa các thông báo lịch hẹn.

**Mô hình C4 - Container**
![b3_client_server_ architecture_image](docs/architecture/c4-container.png)

## 5. Cài đặt và vận hành

### Yêu cầu hệ thống
- Docker Desktop
- Git
- Key dịch vụ Ngrok, Cloudinary, Email Reputation và app-password của tài khoản Google.

### Chạy local nội bộ
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8
    ```
2.  **Chuẩn bị môi trường:** Tạo file .env như mẫu .env.example.
3.  **Khởi chạy theo 1 trong 2 cách:**
    - **Dev:** docker compose up -d --build
    - **Production:** docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

### Chạy dưới dạng web server 
1.  **Clone source code:**
    ```
    git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
    cd Medical-Appointment-B3-8/web-server
    ```
2.  **Chuẩn bị môi trường:** Tạo file .env theo mẫu (bắt buộc).
3.  **Khởi chạy:**
    ```bash
    docker compose -f docker-compose-server.prod.yml up -d --build
    ```
4.  **Lấy URL:** Truy cập http://localhost:7000/status để lấy URL của web app.

## 6. Thông tin truy cập
Các port bên dưới có thể thay đổi tùy cấu hình trong file .env

- **Frontend (Local):** [http://localhost:81](http://localhost:81)
- **Backend API (Local):** [http://localhost:8000](http://localhost:8000)
- **RabbitMQ Management (Local):** [http://localhost:15672](http://localhost:15672)
- **Web app (Production):** [https://resonate-proponent-thrower.ngrok-free.dev](https://resonate-proponent-thrower.ngrok-free.dev) (Tùy thuộc vào ngrok)

## 7. Demo

**Demo:** [Medical-Appointment-Demo](https://drive.google.com/drive/u/0/folders/1DxsuBUrXGs3e7ExIcdaz8nEen7Jye9QF)

## 8. Tài liệu chi tiết
- [ADRs](docs/adrs/)
- [API Documentation](docs/api/)
- [Architecture](docs/architecture/)
- [Hướng dẫn web server](web-server/README.md) 