# ADR-006: Đổi từ cơ chế JWT thuần sang xác thực và phân quyền JWT HttpOnly Method

## Trạng thái
Accepted

## Bối cảnh
Trong thiết kế ban đầu, hệ thống sử dụng cơ chế JWT để xác thực người dùng giữa client và server nhằm đảm bảo tính phi trạng thái stateless. Tuy nhiên, việc lưu trữ token ở phía client bằng localStorage hoặc sessionStorage tiềm ẩn rủi ro bảo mật rất lớn đối với lỗ hổng XSS. Nếu tin tặc chèn được mã độc vào ứng dụng, chúng có thể dễ dàng đọc được token và chiếm quyền điều khiển tài khoản. Vì hệ thống đặt lịch khám đa khoa chứa các thông tin cực kỳ nhạy cảm của bệnh nhân, đặc tính kiến trúc cốt lõi là bảo mật, nên việc đảm bảo xác thực phải được đặt lên hàng đầu để đảm bảo an toàn dữ liệu.

## Quyết định
Chuyển đổi phương thức lưu trữ và truyền tải JWT từ việc client tự lưu sang sử dụng Cookie với cờ HttpOnly, Secure và SameSite. Cụ thể, khi người dùng đăng nhập thành công, Backend sẽ tạo JWT và gắn trực tiếp vào Set-Cookie trong header của HTTP response, Frontend sẽ tự động đính kèm cookie này trong các request tiếp theo thông qua cấu hình withCredentials.

## Lý do
1. Việc thiết lập cờ HttpOnly cho cookie khiến các đoạn mã JavaScript ở phía client hoàn toàn không thể truy cập hay đánh cắp được JWT.
2. Cờ Secure bắt buộc cookie chỉ được truyền đi qua giao thức mã hóa HTTPS, ngăn chặn việc nghe lén token trên đường truyền.
3. Giữ nguyên ưu điểm của kiến trúc: Vẫn duy trì được cơ chế xác thực phi trạng thái của JWT, giúp hệ thống API Server dễ dàng mở rộng ngang (Horizontal Scaling) mà không cần bận tâm đến việc lưu trữ session trên server.
4. Đáp ứng yêu cầu bảo mật khắt khe: Thỏa mãn các kịch bản kiểm tra chất lượng về bảo mật đã được định nghĩa cho nền tảng y tế.


## Hệ quả
1. Tích cực: Tăng cường tối đa độ an toàn cho tài khoản người dùng và bảo mật hồ sơ bệnh án. Giảm bớt gánh nặng quản lý token thủ công ở mã nguồn Frontend. 
2. Tiêu cực: Đánh đổi rủi ro từ XSS sang CSRF. Để khắc phục, hệ thống bắt buộc phải cấu hình thêm thuộc tính SameSite=Strict cho cookie hoặc triển khai thêm cơ chế Anti-CSRF Token. Quá trình cấu hình CORS giữa React và Flask sẽ phức tạp hơn, bắt buộc phải thiết lập Access-Control-Allow-Credentials = true.

## Ngày quyết định
31-03-2026
