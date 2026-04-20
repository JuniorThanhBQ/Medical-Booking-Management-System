# ADR-008: Triển khai web server qua Ngrok tunnel thay vì VPS/PAAS

## Trạng thái
Accepted

## Bối cảnh
Hệ thống đặt lịch khám bệnh trực tuyến đã được đóng gói và vận hành trơn tru ở môi trường cục bộ thông qua một file docker-compose.yml duy nhất. Trong giai đoạn cần đưa hệ thống ra ngoài Internet để khách hàng kiểm thử và demo sản phẩm, việc thuê máy chủ ảo đòi hỏi nhiều công sức cấu hình hạ tầng, trong khi việc chia nhỏ ứng dụng lên các nền tảng PaaS sẽ làm phá vỡ cấu trúc Docker Compose cục bộ hiện tại, gây ra độ trễ mạng và khó khăn trong việc thiết lập kết nối tới các container nội bộ.

## Quyết định
Chấp nhận sử dụng Ngrok tunnel để trực tiếp phơi bày môi trường Docker Compose cục bộ trên máy tính cá nhân của lập trình viên ra ngoài Internet phục vụ cho mục đích kiểm thử và demo, tạm thời hoãn lại phương án triển khai lên VPS hoặc PaaS.

## Lý do
1. Sử dụng Ngrok giúp toàn bộ hệ thống vẫn chạy trên một mạng nội bộ Docker duy nhất. Nhóm không phải tốn thời gian tách nhỏ cấu trúc, thiết lập kết nối database chéo hay lo lắng về độ trễ mạng giữa các dịch vụ phân tán.
2. Giải pháp này giúp loại bỏ hoàn toàn các gánh nặng về mặt vận hành. Không cần cài đặt Web Server, cấu hình Proxy, hay thiết lập CI/CD phức tạp. Chỉ với một câu lệnh khởi chạy Ngrok, một URL an toàn có sẵn HTTPS/TLS sẽ được tự động cấp phát ngay lập tức.
3. Trong quá trình demo hệ thống, nếu xảy ra lỗi, lập trình viên có thể xem trực tiếp log từ terminal nội bộ và sửa lỗi ngay trên máy tính của mình mà không cần SSH lên máy chủ xa.
4. Phù hợp với ngân sách của một đồ án môn học khi Ngrok cung cấp giải pháp miễn phí hoàn toàn, thay vì phải trả phí duy trì hàng tháng cho VPS hoặc các dịch vụ Database Cloud.

## Hệ quả
1. Tích cực: Tiết kiệm tối đa thời gian đưa sản phẩm ra môi trường Internet. Tránh được rào cản quá tải công nghệ ở giai đoạn cần nghiệm thu nhanh. Tự động mã hóa đường truyền giúp bảo mật thông tin truy cập mà không cần phải tự cấu hình SSL/TLS.
2. Tiêu cực: Hệ thống trở thành một "máy chủ tạm thời", phụ thuộc 100% vào máy tính và nguồn điện/mạng của cá nhân lập trình viên. Không thể đáp ứng được các tiêu chuẩn về tính sẵn sàng cho một môi trường Production thực tế. URL thường bị thay đổi sau mỗi lần khởi động lại Ngrok bản miễn phí, gây bất tiện khi phải gửi lại đường link cho người dùng kiểm thử.

## Ngày quyết định
12-04-2026
