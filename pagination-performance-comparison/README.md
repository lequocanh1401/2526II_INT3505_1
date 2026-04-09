# Demo So Sánh Hiệu Năng Các Phương Pháp Pagination

Dự án nhỏ này sử dụng Flask (Python) và SQLite để minh họa và so sánh hiệu năng thực tế của 3 cách tiếp cận Pagination (Phân Trang) phổ biến nhất khi thao tác với lượng dữ liệu lớn (1 triệu bản ghi).

## 3 Phương pháp được áp dụng:

1. **Offset/Limit Pagination**: 
   - Truyền `offset` (Vị trí bắt đầu) và `limit` (Số lượng muốn lấy).
   - *Bản chất*: MySQL/PostgreSQL/SQLite sẽ phải duyệt (scan) tới tận bản ghi có số thứ tự `offset` rồi mới lấy ra `limit` bản ghi. Offset càng lớn, tốc độ query càng chậm.
2. **Page-based Pagination**:
   - Truyền `page` (Số trang) và `size` (Kích thước mỗi trang).
   - *Bản chất*: Đây chỉ là lớp giao diện thân thiện thay thế cho Offset/Limit. SQL đứng dưới vẫn tính toán lại sang OFFSET = `(page - 1) * size`. Do đó, tốc độ và nhược điểm y chang Offset/Limit.
3. **Cursor-based Pagination** (còn gọi là Keyset, Seek Pagination):
   - Truyền `cursor` (Id đánh dấu bản ghi cuối cùng của page cũ) và `limit` (Kích thước mỗi trang).
   - *Bản chất*: Dùng điều kiện so sánh `WHERE id > cursor_id`. Cơ sở dữ liệu sẽ dùng trực tiếp cấu trúc cây Index (B-Tree) để "nhảy" thẳng tới vị trí cần thiết mà không phải scan. Đây là kĩ thuật có tốc độ nhanh và ổn định ở mọi vị trí phân trang.

---

## Hướng dẫn chạy code

Máy bạn cần cài sẵn môi trường Python (chạy Flask và Requests).

Cài các thư viện cần thiết nếu chưa có (thường requests sẽ cần được cài):
```bash
pip install flask requests
```

### Bước 1: Khởi động Server API
Mở một terminal và chạy file `app.py`:

```bash
cd pagination-performance-comparison
python app.py
```
> **Lưu ý**: Trong lần chạy đầu tiên, script sẽ tự động tạo một file `data.db` (SQLite) và cắm vào 1.000.000 bản ghi giả để phục vụ mục đích test. Quá trình này diễn ra khá nhanh do đã được tối ưu transaction. Server sẽ listen ở cổng `5000`.

### Bước 2: Chạy Demo So sánh hiệu năng
Khi server đã chạy (để terminal server đó hoạt động), mở một **terminal mới**, và chạy đoạn mã test:

```bash
cd pagination-performance-comparison
python test_demo.py
```

### Kết quả bạn sẽ thấy
Script `test_demo.py` sẽ in ra một bảng so sánh tốc độ xử lý Query của DB và cả tốc độ gọi HTTP Request thông qua 3 mốc:
- Lấy trang đầu tiên
- Lấy trang ở giữa (bản ghi thứ 500.000)
- Lấy trang cuối cùng (bản ghi thứ 999.990)

Bạn sẽ trực tiếp quan sát được thấy độ chênh lệch thời gian cực lớn giữa `Offset` - `Page-Based` (chậm dần đều theo lượng offset) với `Cursor` (luôn luôn nhanh và giữ vững hiệu năng).
