# Hệ thống đặt lịch khám bệnh (Medical Appointment)

## Mô tả 
Hệ thống cho phép bệnh nhân đặt lịch khám bệnh online, tìm bác sĩ theo chuyên khoa. Hỗ trợ lưu trữ và quản lý hồ sơ bệnh nhân và quản lý bác sĩ, lịch làm việc và theo dõi các lịch khám đã đặt cho các Phòng khám/bệnh viện.

## Thành viên nhóm 
| MSSV | Họ tên | Vai trò | 
|------|--------|---------|
| 2351050164 | Văn Trung Thành | Nhóm trưởng | 
| 2351050133 | Nguyễn Thanh Phong | Thành viên |
| 2351050154 | Trương Hưng Phát | Thành viên |

## Công nghệ sử dụng
- Backend: Flask + RESTful API 
- Frontend: React + Vite 
- Database: MySQL 
- Message Queue: RabbitMQ 
- Container: Docker + Docker Compose 
- Version control: Git + Github 

## Kiến trúc 
Hệ thống đặt lịch khám bệnh được chúng em thiết kế dựa trên mẫu kiến trúc 
Client–Server với phong cách kiến trúc là REST. Trong đó, frontend và backend 
hoạt động độc lập và giao tiếp với nhau dựa trên chuẩn thiết kế RESTful API. 
Đối với phía client, chúng em sử dụng React với Vite để thiết kế và xây dựng 
frontend. Về phía server, chúng em áp dụng kiến trúc phân tầng, công nghệ sử 
dụng cho backend là framework Flask với thư viện Flask-RESTful. Ngoài ra, 
chúng em còn sử dụng MySQL để lưu trữ dữ liệu, RabbitMQ để xử lý các thao 
tác bất đồng bộ, Docker và Docker Compose để đóng gói hệ thống ứng dụng và 
github để kiểm soát phiên bản hệ thống  
![b3_client_server_ architecture_image](docs/architecture/c4-container.png) 

## Cài đặt và chạy 

### Yêu cầu
- Docker Desktop
- Git

### Chạy với Docker Compose 
git clone https://github.com/username/project-name 
cd project-name 
docker-compose up -d 

### Truy cập
- Frontend: http://localhost:5173 
- Backend API: http://localhost:8000 
- RabbitMQ Management: http://localhost:15672 

## Demo 
- [Medical-Appointment-Demo](https://drive.google.com/drive/u/0/folders/1DxsuBUrXGs3e7ExIcdaz8nEen7Jye9QF)

## Tài liệu
- [ADRs](docs/adrs/) 
- [API Documentation](docs/api/) 
- [Architecture](docs/architecture/) 