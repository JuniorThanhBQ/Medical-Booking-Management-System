# ADR-001: Lựa chọn kiến trúc phân lớp (dự kiến)

## Trạng thái
Pending

## Bối cảnh
Nhóm với quy mô thành viên là 3 người, thời gian phân tích cần 2 tuần và thời gian phát triển là 6 tuần. Việc lựa chọn một kiến trúc phải hợp lý cho hệ thống đặt lịch khám bệnh.  

## Quyết định
Sử dụng kiến trúc Layered 3 tầng:
- Presentation Layer (React with ViteJS)
- Business Logic Layer (Flask with RESTful)
- Data Access Layer (Sequelize ORM)

## Lý do
1. Nhóm có kinh nghiệm với kiến trúc phân lớp
2. Các công nghệ đều được nhóm sử dụng qua trong nhiều dự án
2. Các logic từng lớp được tách biệt rõ ràng.
3. Dễ bảo trì và kiểm thử 
4. Phù hợp với phạm vi dự án là "hệ thống đặt lịch"

## Hệ quả
- Tích cực: Dễ quản lý source code trên một thể đơn nhất.
- Tiêu cực: Khó mở rộng khi hệ thống lớn dần và nhiều rủi ro khác gắn liền với kiến trúc phân lớp

## Ngày quyết định
08-02-2026
