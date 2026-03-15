# ADR-003: Lựa chọn hiện thực hóa bằng RESTful API với công nghệ React, Flask và MySQL

## Trạng thái
Accepted

## Bối cảnh
Sau khi chọn mẫu kiến trúc là Client - Server, nhóm so sánh các lựa chọn hiện thực như RESTful API, GraphQL và SOAP và các công nghệ sẽ sử dụng nếu chọn hướng đi đó. Qua trao đổi và đánh giá kinh nghiệm của các thành viên, nhóm quyết định sử dụng RESTful như dự kiến ban đầu với framework React, Flask và hệ quản trị cơ sở dữ liệu MySQL.  

## Quyết định
Sử dụng RESTful API trong hiện thực hệ thống Client - Server với các công nghệ:
1. Framework React với công cụ build Vite.  
2. Framework Flask với thư viện flask-RESTful.  
3. Hệ quản trị cơ sở dữ liệu MySQL.


## Lý do
1. Phù hợp với nguồn lực của nhóm.
2. RESTful API phù hợp cho web applications và mobile APIs. Nguyên tắc đầu tiên của RESTful API là Client - Server nên điều kiện này đã thỏa.  
3. Framework Flask với thư viện flask-RESTful Flask đảm bảo sự đơn giản, dễ cài đặt và mở rộng để giúp nhóm tuân thủ nguyên tắc KISS và tránh bị over-engineering.
4. Giữa React và Next.JS thì nhóm lựa chọn React để đảm bảo tính đơn giản và phù hợp trong khả năng. Bên cạnh đó, việc sử dụng đơn thuần html và css kém hiệu quả hơn so với sử dụng React.
5. MySQL thuộc loại SQL đảm bảo yếu tố ACID cho lưu trữ dữ liệu của hệ thống đặt lịch khám bệnh. 


## Hệ quả
- Tích cực: Thời gian phát triển ngắn và không tốn thời gian học công nghệ mới. Đồng thời, hệ thống sẽ mang các ưu điểm của RESTful API, Flask, React và MySQL.    
- Tiêu cực: Việc lựa chọn Flask cho backend sẽ hạn chế đi các built-in có sẵn so với Django, React sẽ làm giảm trải nghiệm của client vì cần sử tài nguyên phía endpoint và MySQL kém hiệu quả với dữ liệu quy mô lớn. Đồng thời, RESTful API không ép định dạng kiểu dữ liệu đầu ra nên dễ sai kiểu dữ liệu của response.

## Ngày quyết định
15-03-2026
