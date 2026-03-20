# 2526II_INT3505_1 - Week 4: Book API Demo

Dự án này cung cấp một API Quản lý Sách được xây dựng bằng framework Flask và tích hợp tài liệu chuẩn OpenAPI (thông qua Swagger UI).

---

## 🚀 Demo Trực Tuyến
Link demo deploy week4: [https://book-api-demo.vercel.app/api/docs/](https://book-api-demo.vercel.app/api/docs/)

---

## 🛠️ Yêu Cầu Hệ Thống (Prerequisites)
Đảm bảo bạn đã cài đặt phiên bản Python (phiên bản 3.x) trên máy của mình.

---

## ⚙️ Hướng Dẫn Cài Đặt (Local Development)

**Bước 1: Tải mã nguồn**
Clone repository hoặc tải mã nguồn về và di chuyển vào thư mục dự án `Week4`:
```bash
cd Week4
```

**Bước 2: Cấu hình môi trường ảo (Tuỳ chọn nhưng khuyến khích)**
Nên tạo một virtual environment trước khi cài đặt các package:
```bash
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate
```

**Bước 3: Cài đặt các thư viện phụ thuộc**
Từ thư mục `Week4`, chạy lệnh sau để tải các package có trong file `requirements.txt`:
```bash
pip install -r requirements.txt
```

**Bước 4: Khởi chạy ứng dụng**
Khởi chạy server Flask bằng lệnh:
```bash
python app.py
```
Mặc định ứng dụng sẽ chạy cục bộ (local) tại địa chỉ `http://localhost:5000`.

---

## 📖 Hướng Dẫn Sử Dụng API (Swagger UI)
Sau khi ứng dụng đang chạy, hãy mở trình duyệt và truy cập vào đường dẫn sau để xem tương tác trực tiếp với giao diện Swagger UI:  
👉 **[http://localhost:5000/api/docs](http://localhost:5000/api/docs)**

### 📚 Các API Chính Khả Dụng
Dựa trên cấu hình `openapi.yaml`, chúng ta có các endpoint sau để quản lý sách:
- `GET /books`: Lấy danh sách toàn bộ sách
- `POST /books`: Thêm một cuốn sách mới
- `GET /books/{id}`: Lấy thông tin chi tiết một cuốn sách
- `PUT /books/{id}`: Cập nhật thông tin sách
- `DELETE /books/{id}`: Xóa một cuốn sách