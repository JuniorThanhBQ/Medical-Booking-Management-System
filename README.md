# Hệ thống đặt lịch khám bệnh trực tuyến (Medical Appointment B3)

## Mô tả

Hệ thống đặt lịch khám trực tuyến cho phòng khám/bệnh viện: bệnh nhân, lễ tân đặt lịch theo slot thời gian thông qua tìm
kiếm bác sĩ, chuyên khoa và được xem hồ sơ bệnh nhân trong phạm vi cho phép. Bên cạnh đó, bác sĩ có thể quản lý lịch làm
việc và hồ sơ khám bệnh được phụ trách. Ngoài ra, hệ thống tự động nhắc lịch hẹn, admin có quyền quản lý thông tin bác
sĩ và chuyên khoa.

## Thành viên nhóm

| MSSV       | Họ tên             | Vai trò     | Đảm nhiệm |
|------------|--------------------|-------------|-----------|
| 2351050164 | Văn Trung Thành    | Nhóm trưởng | DevOps    |
| 2351050133 | Nguyễn Thanh Phong | Thành viên  | Backend   |
| 2351010154 | Trương Hưng Phát   | Thành viên  | Frontend  |

## Công nghệ sử dụng

### Các công nghệ chính

| Container     | Công nghệ           | Phiên bản                           |
|---------------|---------------------|-------------------------------------|
| Backend       | Flask + Flask-RESTX | Flask: 3.1.3 <br>Flask-RESTX: 1.3.2 |
| Frontend      | React + Vite        | React: 19.2.4 <br>Vite: 7.3.1       |
| Database      | MySQL debian        | Mysql:8.0-debian                    |
| Message Queue | RabbitMQ            | Rabbitmq:4.2.5-management-alpine    |
| Cache         | Redis               | Redis:7-alpine                      |

### Các công nghệ khác

- Container: Docker (v29.3.0) + Docker Compose (v5.1.0)
- Version control: Git (Latest) + GitHub

## Kiến trúc

Hệ thống được thiết kế dựa trên cấu trúc
Client–Server với phong cách kiến trúc là REST. Bốn đặc tính được chọn là tính phù hợp chức năng, bảo mật, độ tin cậy và
hiệu suất. Các quy tắc và hướng dẫn được nhóm trình bày ở mục tài liệu. Trong đó, hệ thống có 5 containers được định
nghĩa và chạy lệnh qua docker-compose.yml. Luồng hoạt động có thể tóm gọn như sau: Client-side (Browser) đến API Server,
từ API Server có thể đi qua Redis (Để lấy url cloudinary và TTL e.g.), MySQL (Database chính và thực hiện truy vấn dữ
liệu nếu Redis nếu không có cache), RabbitMQ (Xử lý bất đồng bộ giữa các thông báo lịch hẹn). Để trực quan, nhóm đã mô
tả containers qua mô hình C4 bên dưới.
<br>   
**Mô hình C4 - Container**
![b3_client_server_ architecture_image](docs/architecture/c4-container.png)

## Cài đặt và chạy

### Yêu cầu

- Docker Desktop
- Git

### Chạy với Docker Compose

- git clone https://github.com/JuniorThanhBQ/Medical-Appointment-B3-8
- cd Medical-Appointment-B3-8
- docker-compose -f docker-compose.prod.yml up -d

### Truy cập

- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- RabbitMQ Management: http://localhost:15672

## Demo

- [Medical-Appointment-Demo](https://drive.google.com/drive/u/0/folders/1DxsuBUrXGs3e7ExIcdaz8nEen7Jye9QF)

## Tài liệu

- [ADRs](docs/adrs/)
- [API Documentation](docs/api/)
- [Architecture](docs/architecture/) 