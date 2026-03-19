# ADR-004: Lựa chọn quy chuẩn coding module

## Trạng thái
Pending

## Bối cảnh
Sau quá trình chọn thiết kế kiến trúc, nhóm chia 3 thành viên ra làm 3 công việc, một bạn CI/CD, một bạn Backend và một bạn Frontend. Dựa trên quyết định pattern cho Server là phân lớp, nhóm cần đưa ra quyết định cách tổ chức source code sao cho phù hợp.

## Quyết định
Sau khi so sánh hai cách thức là tổ chức theo tính năng/module hoặc theo lớp kỹ thuật gộp chung. Nhóm đưa ra quyết định sử dụng cấu trúc hiện thực là coding module.

## Lý do
1. Việc coding theo module/tính năng sẽ giúp cô lập nghiệp vụ cho kiểm thử tốt hơn.
2. Dễ dàng mở rộng nếu sau này có thêm module mới.
3. Đảm bảo tính high cohesion cho tổ chức module, low coupling giữa các module.
4. Dễ phân tách nhiệm vụ. 

## Hệ quả
- Tích cực: Giảm xung đột merge, dễ dàng theo dõi cấu trúc dự án, đảm bảo khả năng kiểm thử và mở rộng.  
- Tiêu cực: Dễ bị vấn đề distributed monolith và sinkhole, cấu trúc folder bốn cấp và nguy cơ lặp code những đoạn đã xử lý ở bên module khác.  

## Ngày quyết định
15-03-2026 (đang chờ thống nhất)
