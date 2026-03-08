# ADR-001: Lựa chọn kiến trúc phân lớp Layered cho hệ thống

## Trạng thái
Rejected

## Bối cảnh
Nhóm với quy mô thành viên là 3 người, thời gian phân tích cần 2 tuần và thời gian phát triển là 6 tuần. Việc lựa chọn một kiến trúc phải hợp lý cho hệ thống đặt lịch khám bệnh. 

### CẬP NHẬT 
Giải pháp đầu tiên được nhóm đề xuất là gom toàn bộ hệ thống vào một khối duy nhất và tổ chức theo Kiến trúc phân tầng.

## Quyết định
Sử dụng kiến trúc Layered 3 tầng:
- Presentation Layer (React with ViteJS)
- Business Logic Layer (Flask with RESTful)
- Data Access Layer (Sequelize ORM)

## Lý do
1. Nhóm có kinh nghiệm với kiến trúc phân lớp
2. Các công nghệ đều được nhóm sử dụng qua trong nhiều dự án
3. Các logic từng lớp được tách biệt rõ ràng.
4. Dễ bảo trì và kiểm thử 
5. Phù hợp với phạm vi dự án là "hệ thống đặt lịch"

### LÝ DO TỪ CHỐI
- Vi phạm tiêu chuẩn REST: nhóm định hướng xây dựng hệ thống giao tiếp qua chuẩn RESTful APIs. Nhưng nếu theo phong cách kiến trúc REST, hệ thống chỉ được sử dụng kiến trúc nguyên khối cho cục bộ frontend hoặc backend. Còn kiến trúc tổng thể phải đáp ứng tiêu chí kiến trúc Client - Server của REST.

## Hệ quả
- Tích cực: Dễ quản lý source code trên một thể đơn nhất.
- Tiêu cực: Khó mở rộng khi hệ thống lớn dần và nhiều rủi ro khác gắn liền với kiến trúc phân lớp

## Ngày quyết định
08-02-2026
