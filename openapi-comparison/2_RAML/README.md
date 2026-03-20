# RAML Demo: Sinh HTML Docs (RAML2HTML)

Định dạng RAML hỗ trợ modeling cấu trúc API rất hiệu quả nhờ `types` và `traits`.

## Hướng dẫn Render HTML
Sử dụng công cụ mã nguồn mở `raml2html` để phân tích (parse) file RAML và sinh ra giao diện HTML tĩnh:

```bash
npx raml2html library.raml > library.html
```
*(Yêu cầu máy chuẩn bị sẵn Node.js)*.

Mở file `library.html` sinh ra để duyệt cấu trúc giao diện phân cấp (hierarchical) theo chuẩn của hệ sinh thái phần mềm MuleSoft.
