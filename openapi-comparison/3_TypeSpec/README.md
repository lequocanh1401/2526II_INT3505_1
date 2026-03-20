# TypeSpec Demo: Compile ra OpenAPI

TypeSpec có ngôn ngữ thiết kế (DSL) tương tự vòng đời phát triển của một ngôn ngữ lập trình như TypeScript. Do Microsoft phát triển để giải quyết việc viết code file Swagger/OpenAPI bằng YAML rất "đau khổ".

## Các bước chạy

**Bước 1: Khởi tạo module npm và cài tool (nếu chưa có node_modules)**
Trong thư mục này, chạy lệnh:
```bash
npm init -y
npm install @typespec/compiler @typespec/http @typespec/rest @typespec/openapi3
```

**Bước 2: Compile TypeSpec file (`main.tsp`)**
Khi biên dịch file main config, TypeSpec sẽ rà soát các decorator và tự động generate ra một file chuẩn OpenAPI v3.
```bash
npx tsp compile main.tsp
```
Sau khi chạy thành công, trình biên dịch sẽ tạo thư mục con mang tên `tsp-output/` → `@typespec/openapi3/`. Trong đó chứa file `openapi.yaml`. 
Bạn có thể dễ dàng lấy file OpenAPI đó đem đi sinh mã server, gắn vào React (Orval), đưa vào Swagger UI hay làm bất kỳ thứ gì hệ sinh thái OpenAPI hỗ trợ!
