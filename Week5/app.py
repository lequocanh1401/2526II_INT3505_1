from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================================
# 1. MOCK DATA (Dữ liệu giả lập)
# ==========================================
# Tạo 25 cuốn sách để test phân trang
books = [
    {"id": i, "title": f"Sách {i}", "category": "IT" if i % 2 == 0 else "Kinh tế", "status": "available" if i % 3 != 0 else "borrowed"}
    for i in range(1, 26)
]

users = {
    1: {"name": "Nguyễn Văn A"},
    2: {"name": "Trần Thị B"}
}

borrowments = [
    {"id": 101, "user_id": 1, "book_id": 2, "borrow_date": "2026-03-01"},
    {"id": 102, "user_id": 1, "book_id": 5, "borrow_date": "2026-03-10"},
    {"id": 103, "user_id": 2, "book_id": 3, "borrow_date": "2026-03-15"},
]

# ==========================================
# 2. ENDPOINTS
# ==========================================

# --- A. TÌM KIẾM & PHÂN TRANG (OFFSET/LIMIT) ---
@app.route('/books', methods=['GET'])
def get_books_offset_pagination():
    # Nhận query parameters
    category = request.args.get('category')
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    # 1. Tìm kiếm / Lọc (Search & Filtering)
    filtered_books = books
    if category:
        filtered_books = [b for b in filtered_books if b['category'] == category]
    if status:
        filtered_books = [b for b in filtered_books if b['status'] == status]

    # 2. Phân trang bằng Offset/Limit
    offset = (page - 1) * limit
    paginated_books = filtered_books[offset : offset + limit]

    return jsonify({
        "total": len(filtered_books),
        "page": page,
        "limit": limit,
        "data": paginated_books
    })

# --- B. PHÂN TRANG (CURSOR-BASED) ---
@app.route('/books/cursor', methods=['GET'])
def get_books_cursor_pagination():
    # Nhận query parameters
    cursor = int(request.args.get('cursor', 0)) # ID của phần tử cuối cùng ở trang trước
    limit = int(request.args.get('limit', 5))

    # Phân trang bằng Cursor (lấy các sách có id > cursor)
    filtered_books = [b for b in books if b['id'] > cursor]
    paginated_books = filtered_books[:limit]

    # Xác định cursor cho trang tiếp theo
    next_cursor = paginated_books[-1]['id'] if paginated_books else None

    return jsonify({
        "next_cursor": next_cursor,
        "limit": limit,
        "data": paginated_books
    })

# --- C. RESOURCE TREE (NESTED RESOURCE) ---
@app.route('/users/<int:user_id>/borrowments', methods=['GET'])
def get_user_borrowments(user_id):
    # Kiểm tra user có tồn tại không
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    # Lọc lịch sử mượn theo user_id
    user_history = [b for b in borrowments if b['user_id'] == user_id]

    return jsonify({
        "user_id": user_id,
        "user_name": users[user_id]["name"],
        "data": user_history
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)