# OpenAPI Demo: Sinh code Server (Code Generation)

Tệp `library.yaml` được định dạng chuẩn OpenAPI v3.

## Hướng dẫn sử dụng OpenAPI Generator
Chúng ta sẽ dùng `@openapitools/openapi-generator-cli` qua công cụ `npx` để tự động sinh sườn ứng dụng server (Python Flask) từ file YAML thiết kế này.

**Bước 1: Chạy lệnh sinh code (Chắc chắn máy đã có cài Node.js)**
```bash
npx @openapitools/openapi-generator-cli generate -i library.yaml -g python-flask -o generated-server
```

**Bước 2: Cài đặt và thử test code vừa sinh ra**
Mở thêm một tiến trình bash, vào thư mục code và thiết lập server:
```bash
cd generated-server
pip install -r requirements.txt
python -m openapi_server
```

**Bước 3: Mở trình duyệt xem Swagger UI (tự sinh)**
Truy cập `http://localhost:8080/ui` để theo dõi API và gửi Request test trên giao diện Swagger UI được thiết lập tự động!
