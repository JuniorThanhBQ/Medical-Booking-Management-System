# Medical Appointment B3 - Web Server

## 1. Các phiên bản

| Tag | Tên | Nội dung |
| :--- | :--- | :--- |
| v2.0.0-test | juniorthanh09/medical-appointment-b3-8-frontend:v2.0.0-test | Images được đẩy lên khi test production (không khuyến khích dùng) | 
| v2.0.0 | juniorthanh09/medical-appointment-b3-8-frontend:v2.0.0 | Images triển khai production đầu tiên và cố định theo thời gian (có thể có bản vá lỗi) |
| latest | juniorthanh09/medical-appointment-b3-8-frontend:latest | Là phiên bản mới nhất được cập nhật thông tin tự động qua pipeline production trên github actions (Khuyên dùng) | 

## 2. Cơ chế hoạt động
Người dùng truy cập Link --> Internet --> Container Ngrok kết nối tunnel giữa người dùng và Nginx --> Nginx định tuyến qua mạng ảo frontend-network bằng tên định danh frontend --> Container Nginx tại cổng nội bộ 8080 điều phối trả về file giao diện tĩnh hoặc API --> Các API định tuyến qua mạng ảo backend-network bằng tên định danh backend --> Container Backend tại cổng nội bộ 8000 xử lý core logic và tương tác với cơ sở dữ liệu.

![b3_web_server_diagram](../docs/architecture/flowchart-web-server.png)

## 3. Một số lưu ý
- Ngrok tunnel đến Nginx, Nginx xử lý proxy giao tiếp giữa các containers (Thuật ngữ cần chú ý) 
- File .env phải đem từ bên ngoài vào trong (copy + paste).
- Mọi biến trong file .env phải cấu hình chuẩn xác để tránh lỗi (nhất là key dịch vụ thứ 3).
- Lệnh chạy server: docker compose -f docker-compose-server.prod.yml up -d --pull always.
- Chỗ này mô phòng thực tế cách thức server hoạt động khi nhánh main có sự thay đổi mới.
- Trong .env, FRONTEND_URL và VITE_API_URL phải để **trống**. 
- Một số lỗi có thể xảy ra bao gồm gãy RabbitMQ hoặc gián đoạn mạng tạm thời do Ngrok miễn phí. 