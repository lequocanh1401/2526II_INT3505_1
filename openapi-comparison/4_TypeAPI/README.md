# TypeAPI Demo

[TypeAPI](https://typeapi.org/) là cấu trúc định dạng JSON Schema-based nhằm mô tả REST APIs nhanh, gọn, đơn giản và thân thiện với việc xây dựng các công cụ sinh mã nguồn (Code Generator) hơn rất nhiều so với OpenAPI.

## Đặc điểm nổi bật
Định dạng TypeAPI chủ yếu dùng file `*.json` có thiết kế phẳng và trực diện, loại bỏ đi triết lý cồng kềnh của OpenAPI/Swagger.

## Hướng dẫn sinh code

Bạn có thể sinh ra Type-Safe Code Client thông qua cộng đồng TypeAPI hoặc nền tảng sdkgen.

```bash
# Ví dụ cài đặt sdkgen
npm install -g @sdkgen/cli

# Chạy lệnh xuất mã nguồn (ví dụ sinh TypeScript interface hoặc Swift, Java client)
# Từ file library.json có sẵn trong thư mục này
```
*(Hệ sinh thái của TypeAPI rất hữu ích khi tập trung sinh ra các REST Client, Type-safe Fetcher cho các frontend client thay vì sinh mã Server như OpenAPI Generator).*
