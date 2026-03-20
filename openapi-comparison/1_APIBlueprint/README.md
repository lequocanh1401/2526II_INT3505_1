# API Blueprint Demo: Chạy Test / Render HTML

Định dạng API Blueprint (.apib) dựa trên Markdown giúp việc viết tài liệu rất giống văn xuôi thông thường.

## 1. Sinh giao diện HTML với Aglio
Aglio là công cụ giúp build file `.apib` thành một trang tài liệu tĩnh (HTML) tuyệt đẹp.
```bash
npx aglio -i library.apib -o library.html
```
Sau đó mở file `library.html` trên trình duyệt.

## 2. Test tự động với Dredd
Dredd là một HTTP API Testing framework cực kỳ mạnh mẽ, được sinh ra cho API Blueprint (hỗ trợ cả OpenAPI). Nó cho phép gọi test trực tiếp từ tài liệu:
```bash
# Yêu cầu máy cài sẵn Nodejs
npx dredd library.apib http://localhost:8080
```
(Chú ý: Cần có 1 server đang chạy thực sự ở port 8080 theo chuẩn thiết kế để Dredd request đến test xem response đúng hay sai).
