# ADR-004: Lựa chọn mẫu kiến trúc cho backend là Layered

## Trạng thái
Accepted

## Bối cảnh
Backend được hiện thực hóa bằng framework Flask kết hợp thư viện Flask-RESTful để cung cấp các RESTful API cho ứng dụng React. Phía cơ sở dữ liệu sử dụng MySQL. Để đảm bảo source code của backend được tổ chức một cách khoa học, dễ quản lý, dễ kiểm thử thì chúng tôi lựa chọn mẫu kiến trúc phân tầng. 

## Quyết định
Sử dụng kiến trúc phân tầng gồm 3 layers chính để tổ chức source code cho hệ thống backend chia theo từng modules. Cụ thể:
1. Presentation Layer (views.py): Chịu trách nhiệm cấu hình các API endpoints bằng Flask-RESTful, tiếp nhận request từ Client, kiểm tra tính hợp lệ của đầu vào và trả về response.
2. Business Logic Layer (services.py): Chứa toàn bộ các quy tắc nghiệp vụ cốt lõi của hệ thống.
3. Data Access Layer (repositories.py): Sử dụng SQLAlchemy ORM để quản lý giao tiếp, truy vấn và thực hiện các thao tác CRUD trực tiếp xuống cơ sở dữ liệu MySQL.
4. Ngoài ra còn có routers layer để định tuyến các views.  

## Lý do
1. Tách biệt mối quan tâm, mỗi tầng giải quyết một vấn đề cụ thể. Tầng Controller chỉ lo giao tiếp HTTP, tầng Service lo nghiệp vụ, tầng Data Access lo thao tác DB. Điều này giúp giảm sự phụ thuộc giữa các thành phần.
2. Dễ bảo trì và nâng cấp ở một tầng, sự thay đổi sẽ ít ảnh hưởng hoặc không ảnh hưởng đến các tầng phía trên.
3. Dễ kiểm thử và viết unit test độc lập cho từng tầng, đặc biệt là tầng Business Logic, bằng cách giả lập các đối tượng phụ thuộc ở tầng Data Access
4. Phù hợp với nguồn lực và công nghệ, có cấu trúc tự nhiên, thân thiện và dễ tiếp cận đối với các thành viên trong nhóm đang làm quen với thiết kế hệ thống.


## Hệ quả
1. Tích cực: Source code được tổ chức gọn gàng, rõ ràng. Khả năng tái sử dụng cao, tầng business Logic có thể được dùng chung cho nhiều Controller khác nhau
2. Tiêu cực: Hiệu suất có thể bị ảnh hưởng nhẹ do dữ liệu phải đi qua nhiều lớp trung gian. Có thể dẫn đến anti-pattern "Architecture Sinkhole" khi các request đọc dữ liệu đơn giản vẫn phải đi xuyên qua 3 tầng mà không có bất kỳ xử lý logic nào ở tầng Service, gây lãng phí code 
3. Vì bản chất vẫn là một ứng dụng Monolithic phân tầng, khả năng mở rộng linh hoạt theo từng module sẽ bị hạn chế, sau này nếu hệ thống lớn lên sẽ phải nhân bản toàn bộ ứng dụng.

## Ngày quyết định
17-03-2026
