# ADR-002: Lựa chọn kiến trúc Client - Server cho hệ thống và kiến trúc phân lớp cho Server

## Trạng thái
Accepted

## Bối cảnh
Quy mô thành viên của nhóm là 3 người. Thời gian để hiện thực, kiểm thử, triển khai và vận hành hệ thống là 5 tuần. Kinh nghiệm của nhóm tập trung vào khai thác và vận dụng API, cũng như là phát triển các ứng dụng thuộc Client - Server. Vì vậy, nhóm đề xuất sử dụng kiến trúc Client - Server

## Quyết định
Sử dụng kiến trúc Client - Server:
- Client (React + Vite, triển khai trên Vercel)
- Server (Flask + Flask-RESTful, triển khai trên PythonAnywhere)

Sử dụng kiến trúc Layered 3 tầng cho Server:
- Presentation Layer (Controller)
- Business Logic Layer (Service)
- Data Access Layer (SQLAlchemy ORM)

## Lý do
1. Mô hình Client-Server đáp ứng nguyên tắc RESTful API.
2. Tăng sự hiệu quả trong phát triển ứng dựng. Một bạn phát triển backend, frontend và CI/CD merge ứng dụng. 
3. Đảm bảo tính nhất quán dữ liệu và các ưu điểm của kiến trúc Client-Server.
4. Việc sử dụng kiến trúc Layered ở backend giúp quản lý code và unit test cho từng chức năng.
5. Phù hợp với khả năng và kinh nghiệm của nhóm

## Hệ quả
- Tích cực: Linh hoạt trong thay đổi nghiệp vụ và chức năng, tách biệt ràng buộc hệ thống. Nếu phía client bị lỗi thì server vẫn hoạt động bình thường, tránh được rủi ro client và server sập cùng lúc.
- Tiêu cực: Đối với hệ thống, nó sẽ mang những nhược điểm của kiến trúc phân tán như độ trễ của mạng. Còn backend thì sẽ gặp hiện tượng sinkhole, god object và tính sẵn sàng không đảm bảo.

## Ngày quyết định
08-02-2026
