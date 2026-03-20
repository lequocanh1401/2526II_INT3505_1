# Nội dung chi tiết so sánh (Slide Content)

Tài liệu này dùng để nắm bắt lý thuyết, chuẩn bị trước các thông tin phân tích để trình bày/tạo slide.

## 1. OpenAPI (trước đây là Swagger)
- **Định dạng code:** YAML hoặc JSON.
- **Ưu điểm nổi bật:**
  - Trở thành tiêu chuẩn "bất thành văn" (de facto standard) cho hầu hết tất cả thiết kế RESTful APIs ngày nay.
  - Hệ sinh thái công cụ lớn nhất thế giới (OpenAPI Generator, Swagger UI, tương thích sâu với Postman, Insomnia,...).
  - Tự động sinh code (mã nguồn máy chủ/máy khách) trơn tru, giảm tải lượng công việc lặp lại.
- **Nhược điểm cốt lõi:** 
  - Khó duy trì khi project phình to: cấu hình YAML thụt dòng dễ nhầm, cấu trúc có xu hướng lặp lại nếu không lạm dụng keyword `$ref`.
- **Đề xuất áp dụng:** Mặc định nên sử dụng với mọi dự án cần cung cấp Endpoint cho bên thứ ba, hoặc cho Microservices.

---

## 2. API Blueprint
- **Định dạng code:** Markdown (kết hợp tiêu chuẩn MSON).
- **Ưu điểm nổi bật:** 
  - Triết lý "Document-First" hoàn toàn triệt để: văn bản thiết kế của Blueprint rất giống một đoạn blog Markdown. Con người có thể đọc hiểu nó không cần bất kì Tool giao diện (UI) nào trích xuất (Render).
  - Cực kỳ hữu dụng để Review tài liệu thiết kế giữa Developer và Business, Product Owner.
- **Nhược điểm cốt lõi:** 
  - Không mạnh trong khoản sinh code. Cộng đồng duy trì có dấu hiệu giảm sút, thua thiệt các công cụ sinh sinh lực mới của OpenAPI.
- **Đề xuất áp dụng:** Sử dụng trong nhóm nhỏ, thích sự tối giản về mặt Docs.

---

## 3. RAML (RESTful API Modeling Language)
- **Định dạng code:** YAML.
- **Ưu điểm nổi bật:** 
  - Rất trực quan trong việc thiết kế các cấu trúc URL lồng nhau (hierarchical/nested).
  - Khả năng đóng gói thành modules đỉnh cao nhờ vào từ khóa `types` và `traits`, giúp mã thiết kế mang tính "Lập trình đối tượng" và DRY (Don't Repeat Yourself) rất cao.
- **Nhược điểm cốt lõi:** 
  - Sự tồn tại phụ thuộc nặng vào nền tảng thiết kế quản lý API của Enterprise MuleSoft.
  - Đặc tính Module hoá của RAML kể từ khi OpenAPI v3 cải tiến đã không còn là lợi thế độc quyền lớn nhất nữa.
- **Đề xuất áp dụng:** Các doanh nghiệp đang tận dụng hoàn toàn hệ sinh thái của MuleSoft Integration, hay kiến trúc API cực sâu.

---

## 4. TypeSpec (từ Microsoft)
- **Định dạng code:** Cú pháp biên dịch tuỳ chỉnh (giống TypeScript hoặc C#).
- **Ưu điểm nổi bật:** 
  - Thiết kế trải nghiệm lập trình viên (Developer Experience) mạnh mẽ nhất. Cho phép viết API specifications thông qua cấu trúc lập trình hướng đối tượng, an toàn kiểu (type-safety).
  - Hoạt động giống một Compiler: source code TypeSpec sẽ tự động *dịch* để nhả ra đầu cuối là các tệp hợp chuẩn định dạng như OpenAPI (Swagger), Protobuf, thay vì viết chúng thủ công.
- **Nhược điểm cốt lõi:** 
  - Đường cong học tập lâu: Phải làm quen với ngôn ngữ TypeSpec mới. Tích hợp với TypeScript tooling vẫn còn cần cải tiến dần.
- **Đề xuất áp dụng:** Đội dự án Developer đang sử dụng TypeScript, muốn thiết kế API Specs chuyên biệt nhanh chóng mà không phải đau đầu bởi các lỗi cú pháp YAML rườm rà.

---

## 5. TypeAPI
- **Định dạng code:** JSON.
- **Ưu điểm nổi bật:** 
  - Đơn giản hóa hoàn toàn kiến trúc của OpenAPI. Cấu trúc gần giống AST (Abstract Syntax Tree) nên viết tool sinh code cực kỳ dễ.
  - Phù hợp hoàn hảo để tạo Type-Safe REST Client cho Frontend Client và Mobile Apps cực nhanh.
- **Nhược điểm cốt lõi:** 
  - Vẫn còn xa lạ với phần đông kỹ sư backend. Thiếu giao diện hiển thị Docs ăn liền đẹp như UI của Swagger hay ReDoc do cấu trúc cộng đồng thiên về công cụ sinh mã.
- **Đề xuất áp dụng:** Ứng dụng Frontend hoặc Fullstack Nodejs/TS không cần UI quá rườm rà nhưng dồn trọng tâm vào việc sinh Type-safe fetch/query tự động hiệu quả từ API endpoint.
