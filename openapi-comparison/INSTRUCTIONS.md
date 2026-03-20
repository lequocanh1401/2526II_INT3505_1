# Hướng dẫn và Yêu cầu (Instructions)

## 1. Mục đích
So sánh các định dạng và ngôn ngữ thiết kế API (API Description Formats) phổ biến hiện nay bao gồm: OpenAPI, API Blueprint, RAML và TypeSpec. Qua đó, giúp người học phân biệt, đánh giá ưu/nhược điểm và lựa chọn công cụ phù hợp cho các dự án thực tế.

## 2. Yêu cầu chuyên môn
- Trình bày điểm đặc trưng của từng format.
- Phân tích cú pháp, ưu điểm, nhược điểm, và hệ sinh thái công cụ hỗ trợ.
- Triển khai một Demo ứng dụng API Quản lý Thư viện (Library Management API) cơ bản làm chuẩn tương đồng để dễ dàng đối chiếu.

## 3. Nội dung Demo
- Cấu trúc tài nguyên API được áp dụng đồng nhất cho các chuẩn:
  - `GET /books`: Lấy danh sách toàn bộ sách hiện có.
  - `POST /books`: Thêm một dữ liệu sách mới.
  - `GET /books/{id}`: Xem chi tiết thông tin một cuốn sách theo ID.
- Demo việc tự động hóa (sinh code server/test API) để thấy rõ khác biệt định dạng trong thực tế.

## 4. Phân bổ cấu trúc thư mục
Các thư mục tương ứng cung cấp code ví dụ và hướng dẫn (README riêng của từng phần):
- **0_OpenAPI**: Định dạng tiêu chuẩn `.yaml` và ví dụ tự sinh mã nguồn server (Python Flask) qua công cụ OpenAPI Generator.
- **1_APIBlueprint**: Định dạng Markdown `.apib` và ví dụ test tự động giao tiếp HTTP thông qua Testing Framework (Dredd).
- **2_RAML**: Định dạng YAML phân nhánh cấu trúc `.raml` và ví dụ xuất giao diện UI tài liệu (HTML tĩnh).
- **3_TypeSpec**: Viết tài liệu bằng file `.tsp` kiểu TypeScript, minh chứng quá trình compiler (biên dịch) xuất ngược trở lại về OpenAPI chuẩn.
- **4_TypeAPI**: Định dạng JSON mở rộng `.json`, nhằm tối giản hóa những nhược điểm thiết kế của OpenAPI và minh họa tiện lợi cho việc render code Type-Safe REST Client.
