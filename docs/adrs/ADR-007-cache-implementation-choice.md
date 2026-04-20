# ADR-007: Chuyển đổi cơ chế lưu trữ từ container memory sang Redis

## Trạng thái
Accepted

## Bối cảnh
Loại bỏ việc lưu trữ trạng thái và dữ liệu tạm thời ở bộ nhớ cục bộ của các container backend. Chuyển đổi sang lưu trữ tại hệ thống cache trung tâm là Redis được triển khai dưới dạng container độc lập bên trong mạng Docker Compose của dự án

## Quyết định
Sử dụng Redis làm hệ thống cache trung tâm để lưu trữ các trạng thái, dữ liệu tạm thời và bộ đệm cấu hình. Redis sẽ được định nghĩa là một service độc lập bên trong tệp docker-compose.yml và giao tiếp với backend thông qua mạng nội bộ của Docker Compose

## Lý do
1. Các Docker container có bản chất tạm thời. Dữ liệu được lưu trực tiếp trên bộ nhớ cục bộ hoặc lớp ghi của container sẽ bị mất hoàn toàn khi container đó bị dừng hoặc xóa.
2. Để hệ thống có khả năng mở rộng ngang bằng cách nhân bản thêm nhiều API containers, các container này bắt buộc phải stateless
3. Nếu lưu trạng thái ở RAM cục bộ, người dùng sẽ gặp lỗi dữ liệu không đồng bộ khi Load Balancer chuyển hướng request sang các container khác nhau. 
4. Redis là cơ sở dữ liệu in-memory giúp giảm tải cho cơ sở dữ liệu chính, cung cấp thời gian phản hồi cực kỳ thấp cho các thao tác đọc dữ liệu thường xuyên.

## Hệ quả
1. Tích cực: Giải quyết triệt để vấn đề mất dữ liệu và bất đồng bộ khi vận hành nhiều bản sao backend. Cải thiện đáng kể hiệu năng tổng thể của ứng dụng. Service backend có thể dễ dàng gọi Redis qua tên  service và dữ liệu cache có thể được lưu trữ bền vững nếu gắn thêm Named Volume
2. Tiêu cực: Tăng độ phức tạp của hạ tầng và vận hành, vì nhóm phải quản lý, cấu hình và giám sát thêm một service mới trong cụm Docker Compose. Các lập trình viên phải thiết kế thêm các chiến lược làm mới bộ đệm hợp lý để tránh tình trạng hệ thống trả về dữ liệu cũ.

## Ngày quyết định
07-04-2026
