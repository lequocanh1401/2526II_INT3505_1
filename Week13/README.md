# 🚀 API as a Product - Kiến trúc hướng dịch vụ (SOA)

## 📌 1. Giới thiệu bài toán & Bối cảnh
Dự án này được xây dựng nhằm minh họa thực tế cho nội dung bài học **"API as a Product"** (Buổi 13 - Môn Kiến trúc hướng dịch vụ). 

Thay vì chỉ coi API là một công cụ kỹ thuật thuần túy để kết nối Front-end và Back-end, đồ án này tiếp cận API dưới góc nhìn **Thương mại (Business/Product)**: Xem API là một sản phẩm mang lại giá trị trực tiếp cho khách hàng (Developers), có mô hình kiếm tiền riêng, có trải nghiệm người dùng đặc thù và cần các chỉ số đo lường hiệu năng kinh doanh (KPIs).

---

## 🛠️ 2. Công nghệ sử dụng & Kiến trúc hệ thống
- **Ngôn ngữ chính:** Python 3.x
- **Framework:** Flask (Gọn nhẹ, tối ưu cho việc xây dựng Microservices và RESTful API)
- **Kiến trúc dữ liệu:** Bộ nhớ tạm (In-memory Dictionary) mô phỏng Database để tối giản hóa việc cài đặt và tập trung hoàn toàn vào luồng xử lý logic của API.

### Sơ đồ luồng xử lý (API Workflow)
1. **Client** gửi request kèm API Key qua HTTP Header (`X-API-KEY`).
2. **Core API Service** kiểm tra tính hợp lệ của Key (Xác thực - Authentication).
3. Hệ thống đối chiếu với gói cước (**Monetization Tier**) để kiểm tra giới hạn lượt gọi (**Rate Limiting**).
4. Nếu hợp lệ, hệ thống xử lý dữ liệu, cập nhật bộ đếm và trả về kết quả `200 OK`.
5. Mọi hành vi (thành công/thất bại) đều được ghi nhận vào bộ nhớ đo lường (**Analytics Engine**) để tính toán KPIs.

---

## ✨ 3. Chi tiết các tính năng cốt lõi

### 🔹 Developer Experience (DX) - Trải nghiệm Lập trình viên
API được thiết kế hướng tới sự tường minh và dễ tích hợp:
- **Chuẩn hóa thông điệp lỗi:** Định dạng JSON nhất quán.
- **Mã lỗi HTTP chuẩn RESTful:** Trả về `401 Unauthorized` khi thiếu/sai token, giúp Client phân biệt rõ ràng lỗi cấu hình của họ với lỗi hệ thống (`500`).
- **Nội dung thông báo (Message):** Chỉ dẫn chi tiết cách sửa lỗi (*"Please check 'X-API-KEY' header"*).

### 🔹 Monetization - Mô hình kinh doanh & Phân loại gói cước
Hệ thống phân hóa tài nguyên dựa trên giá trị thương mại thương lượng với đối tác:
- **Free Tier (`free`):** Giới hạn tối đa **3 requests**. Thích hợp cho việc thử nghiệm (Sandbox). Khi vượt quá, hệ thống trả về mã lỗi `429 Too Many Requests`.
- **Premium Tier (`premium`):** Hạn mức cao hơn (**100 requests**), dành cho khách hàng trả phí để vận hành thực tế.

### 🔹 KPIs & Analytics - Đo lường hiệu năng sản phẩm
Cung cấp một Endpoint nội bộ dành riêng cho Product Manager theo dõi sức khỏe của sản phẩm API thông qua 3 chỉ số KPIs chính:
- **Registered Developers Count:** Tổng số lập trình viên/đối tác đã đăng ký hệ thống.
- **Total Call Volume:** Tổng lưu lượng truy cập hệ thống (đánh giá tải và mức độ tăng trưởng).
- **Error Rate (%):** Tỷ lệ các cuộc gọi lỗi trên tổng số cuộc gọi. Chỉ số này giúp phát hiện bất thường hệ thống hoặc hành vi lạm dụng API của người dùng Free.

---

## 🔌 4. Tài liệu chi tiết các API Endpoints (API Specifications)

### 1. Core API Service (Sản phẩm bán cho khách hàng)
* **URL:** `/api/v1/data`
* **Method:** `GET`
* **Headers bắt buộc:** `X-API-KEY` (Dùng để định danh Developer)
* **Phản hồi mẫu thành công (200 OK):**
  ```json
  {
    "status": "success",
    "developer": "Anh Le",
    "tier_used": "premium",
    "remaining_requests": 99,
    "data": "Đây là dữ liệu giá trị cao từ sản phẩm API của bạn!"
  }