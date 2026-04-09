from flask import Flask, request, jsonify
import sqlite3
import time
import os

app = Flask(__name__)
DB_FILE = "data.db"
TOTAL_RECORDS = 1000000  # Tạo 1 triệu bản ghi để có thể thấy rõ sự khác biệt hiệu năng

def get_db():
    conn = sqlite3.connect(DB_FILE)
    # Lấy dữ liệu dưới dạng dictionary thay vì tuple để dễ parse JSON
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Hàm khởi tạo cơ sở dữ liệu giả nếu chưa có"""
    if os.path.exists(DB_FILE):
        return
    print(f"Đang tạo cơ sở dữ liệu với {TOTAL_RECORDS} bản ghi... Vui lòng đợi vài giây.")
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    value INTEGER
                 )''')
    
    # Chèn dữ liệu giả. Dùng transaction để insert nhanh
    data = [(f"Item {i}", i) for i in range(1, TOTAL_RECORDS + 1)]
    c.executemany("INSERT INTO items (name, value) VALUES (?, ?)", data)
    conn.commit()
    
    # Tạo Index cho ID để tối ưu hóa truy vấn có điều kiện (Quan trọng cho Cursor-based)
    c.execute("CREATE INDEX idx_items_id ON items(id)")
    conn.commit()
    conn.close()
    print("Tạo dữ liệu thành công!")

# ==============================================================================
# PHƯƠNG PHÁP 1: OFFSET / LIMIT
# ==============================================================================
@app.route('/api/offset', methods=['GET'])
def pagination_offset_limit():
    """
    Sử dụng từ khóa LIMIT và OFFSET của SQL.
    Nhược điểm lớn nhất là CSDL phải duyệt qua tất cả các dòng từ đầu cho đến khi đạt `offset`.
    Càng lấy dữ liệu ở sâu (offset càng lớn) thì càng CHẬM.
    """
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    start_time = time.time()
    conn = get_db()
    c = conn.cursor()
    # Query bắt CSDL quét và bỏ qua `offset` bản ghi đầu tiên
    c.execute("SELECT * FROM items ORDER BY id ASC LIMIT ? OFFSET ?", (limit, offset))
    rows = c.fetchall()
    conn.close()
    
    # Đo thời gian chỉ riêng cho câu Query DB
    duration = time.time() - start_time
    
    return jsonify({
        'data': [dict(r) for r in rows],
        'execution_time_seconds': duration,
        'method': 'offset_limit'
    })

# ==============================================================================
# PHƯƠNG PHÁP 2: PAGE-BASED
# ==============================================================================
@app.route('/api/page', methods=['GET'])
def pagination_page_based():
    """
    Tương tự như Offset/Limit, nhưng thân thiện hơn với người dùng (Truyền vào `page` thay vì `offset`).
    Bản chất truy vấn SQL ở dưới vẫn sử dụng LIMIT và OFFSET (offset = (page-1)*size).
    Do đó hiệu năng CHẬM tương đương Offset/Limit ở các trang sâu.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    
    # Tính toán offset từ page
    offset = (page - 1) * size
    
    start_time = time.time()
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id ASC LIMIT ? OFFSET ?", (size, offset))
    rows = c.fetchall()
    conn.close()
    
    duration = time.time() - start_time
    
    return jsonify({
        'data': [dict(r) for r in rows],
        'execution_time_seconds': duration,
        'method': 'page_based',
        'current_page': page
    })

# ==============================================================================
# PHƯƠNG PHÁP 3: CURSOR-BASED (KEYSET)
# ==============================================================================
@app.route('/api/cursor', methods=['GET'])
def pagination_cursor():
    """
    Dùng điểm đánh dấu (cursor), thường là ID của bản ghi cuối cùng của lần fetch trước.
    Thay vì bắt CSDL quét rồi bỏ qua offset, chúng ta bảo CSDL: 
    "Hãy tìm ID lớn hơn cái ID này, lấy N bản ghi".
    Kết hợp với việc đánh INDEX (Chỉ mục) trên cột ID, tốc độ TÌM KIẾM CỰC NHANH và ổn định ở mọi vị trí.
    """
    limit = int(request.args.get('limit', 10))
    cursor = int(request.args.get('cursor', 0)) # Mặc định 0 để bắt đầu từ bản ghi đầu tiên
    
    start_time = time.time()
    conn = get_db()
    c = conn.cursor()
    # Dùng WHERE id > ? để tận dụng trực tiếp Index tree (B-Tree) của CSDL
    c.execute("SELECT * FROM items WHERE id > ? ORDER BY id ASC LIMIT ?", (cursor, limit))
    rows = c.fetchall()
    conn.close()
    
    duration = time.time() - start_time
    
    # Trả về ID của phần tử cuối cùng để client có thể dùng cho đợt fetch tiếp theo
    next_cursor = rows[-1]['id'] if rows else None
    
    return jsonify({
        'data': [dict(r) for r in rows],
        'execution_time_seconds': duration,
        'method': 'cursor_based',
        'next_cursor': next_cursor
    })


if __name__ == '__main__':
    init_db()  # Tạo dữ liệu nếu chưa có
    print("\n--- Server đang chạy tại http://127.0.0.1:5000 ---")
    print("Hãy mở terminal khác và chạy: python test_demo.py\n")
    app.run(debug=True, port=5000)
