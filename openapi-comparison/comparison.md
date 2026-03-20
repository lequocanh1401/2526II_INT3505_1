# So Sánh Các Định Dạng Tài Liệu Hóa API (API Description Formats)

Trong việc thiết kế và tài liệu hóa API, có 4 định dạng phổ biến thường được nhắc tới: **OpenAPI (Swagger)**, **API Blueprint**, **RAML**, và **TypeSpec**. Dưới đây là phân tích và so sánh nhanh từng công cụ, cùng với demo cho ứng dụng Quản lý Thư viện (Library Management).

## 1. OpenAPI (trước đây là Swagger)
- **Định dạng:** YAML hoặc JSON.
- **Ưu điểm:** Tiêu chuẩn công nghiệp (de facto standard) cho RESTful APIs. Hệ sinh thái khổng lồ (OpenAPI Generator, Swagger UI, Postman, v.v.). Hỗ trợ mạnh mẽ việc sinh code (code generation) cho cả server và client.
- **Nhược điểm:** Cú pháp đôi khi khá dài dòng và lặp lại (nếu không dùng `$ref` tốt). Dễ bị "rối" với các API lớn nếu không cấu trúc thư mục hợp lý.
- **Sử dụng khi:** Muốn chuẩn hóa API rộng rãi, sinh code tự động, cần cộng đồng hỗ trợ lớn.

## 2. API Blueprint
- **Định dạng:** Markdown-based (Markdown kết hợp MSON).
- **Ưu điểm:** Cực kỳ dễ đọc và viết cho con người vì nó giống văn bản bình thường. Phù hợp cho việc thiết kế theo hướng Design-First và chia sẻ trực tiếp với stakeholders (non-technical).
- **Nhược điểm:** Hệ sinh thái nhỏ, ít công cụ liên kết trực tiếp để sinh ra code tốt bằng OpenAPI.
- **Sử dụng khi:** Chú trọng vào tính đọc-hiểu của tài liệu, hoặc làm tài liệu API public trước khi chuyển giao.

## 3. RAML (RESTful API Modeling Language)
- **Định dạng:** YAML.
- **Ưu điểm:** Thiết kế thông minh theo hướng cấu trúc phân cấp (hierarchical), hỗ trợ kế thừa `traits` và `types` giúp tái sử dụng mã rất tự nhiên. 
- **Nhược điểm:** Liên kết chặt chẽ phần lớn ở xung quanh hệ thống MuleSoft. Phiên bản OpenAPI v3+ đã bắt kịp các chức năng tái sử dụng nên RAML hiện nay không phổ biến bằng.
- **Sử dụng khi:** API cực lớn, kiến trúc phức tạp, cần mô hình hóa resource một cách tường minh qua cây thư mục, hoặc sử dụng MuleSoft platform.

## 4. TypeSpec (từ Microsoft)
- **Định dạng:** Cú pháp giống TypeScript (.tsp).
- **Ưu điểm:** Developer experience tuyệt vời. Cú pháp gọn gàng, kế thừa linh hoạt, type-safe (an toàn kiểu). Code rất trong sáng. Sau đó có trình biên dịch để xuất ra ngay file chuẩn OpenAPI v3/3.1, Protobuf...
- **Nhược điểm:** Đòi hỏi phải học thêm cách viết syntax compiler mới của tool.
- **Sử dụng khi:** Đội ngũ developer quen sử dụng TypeScript/C#, viết API specifications nhanh chóng và không thích xử lý cú pháp thụt lề tốn thời gian của YAML.

---

## 🚀 Demo: Ứng dụng Quản lý Thư viện
Bên dưới thư mục `openapi-comparison` chia sẵn các folder ứng với 4 định dạng trên. Các API ví dụ gồm có:
- `GET /books`: Liệt kê sách
- `POST /books`: Thêm sách mới
- `GET /books/{id}`: Xem chi tiết sách

Vui lòng điều hướng vào các folder con để xem file ngôn ngữ thiết kế API tương ứng và hướng dẫn chạy công cụ sinh code (hoặc test):
1. [OpenAPI](./openapi)
2. [API Blueprint](./api-blueprint)
3. [RAML](./raml)
4. [TypeSpec](./typespec)
