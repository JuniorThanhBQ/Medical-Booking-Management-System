# ADR-005: Lựa chọn mẫu Message Broker để xử lý nhắc lịch hẹn

## Trạng thái
Accepted

## Bối cảnh
Trong hệ thống đặt lịch khám bệnh trực tuyến, tính năng nhắc lịch hẹn và thông báo sự cố yêu cầu hệ thống phải gửi email cho bệnh nhân. Việc gọi đồng bộ dịch vụ gửi email ngay trong lúc người dùng hoặc lễ tân thao tác gọi API sẽ làm tăng thời gian phản hồi và làm giảm trải nghiệm người dùng. Hơn nữa, nếu dịch vụ email bên thứ 3 gặp sự cố, luồng đặt lịch chính có thể bị lỗi theo. Do đó, hệ thống cần áp dụng cơ chế hàng đợi sự kiện để xử lý các tác vụ này qua Message Broker.

## Quyết định
Sử dụng Message Broker để quản lý hàng đợi và xử lý bất đồng bộ các tác vụ nhắc lịch hẹn, gửi thông báo thay đổi lịch khám cho bệnh nhân.

## Lý do
1. Phù hợp với tính chất hệ thống: Message Broker truyền thống hoạt động dựa trên cơ chế "Smart broker, dumb consumer", cung cấp khả năng định tuyến phức tạp rất phù hợp với việc phân loại các tin nhắn nhắc lịch, hủy lịch hay tạo hồ sơ.
2. Độ tin cậy cao vì gửi nhận có xác nhận, đảm bảo các thông báo nhắc lịch quan trọng được giao tới đích và không bị rơi rớt khi hệ thống gặp sự cố.
3. Phân tách trách nhiệm Core Service chỉ cần đẩy sự kiện theo cơ chế "Fire and Forget" và trả ngay phản hồi cho khách hàng, giúp hệ thống không bị nghẽn mạng.

## Hệ quả
1. Tích cực: Tách biệt hoàn toàn luồng nghiệp vụ lõi với luồng gửi thông báo, giúp thời gian phản hồi của API cực kỳ nhanh chóng. Hệ thống có thể hoạt động bền bỉ, dễ dàng cấu hình Retry hoặc Dead Letter Queue nếu gửi mail thất bại
2. Tiêu cực: Làm tăng độ phức tạp của kiến trúc tổng thể vì phải triển khai và giám sát thêm một thành phần hạ tầng mới của Message Broker. Quá trình gỡ lỗi tin nhắn bất đồng bộ cũng khó khăn hơn so với gọi API đồng bộ, đòi hỏi kiến thức vận hành chuyển sâu để tránh điểm chết duy nhất (Single Point of Failure)

## Ngày quyết định
22-03-2026
