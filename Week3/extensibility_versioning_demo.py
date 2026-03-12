from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập database có nhiều phim
films_db = [{"id": i, "title": f"Film {i}"} for i in range(1, 101)]

# --- VERSION 1: THIẾT KẾ CŨ (Hạn chế về tính mở rộng) ---
@app.route('/api/v1/films', methods=['GET'])
def get_films_v1():
    # Trả về toàn bộ 100 phim (Dễ làm sập server nếu database có 1 triệu phim) 
    return jsonify({
        "status": "success",
        "version": "v1",
        "data": films_db 
    }), 200


# --- VERSION 2: THIẾT KẾ MỚI (Dễ mở rộng - Extensibility) ---
# Thêm tính năng Phân trang (Pagination) và Lọc (Filtering) [cite: 62-63, 142-143]
@app.route('/api/v2/films', methods=['GET'])
def get_films_v2():
    # Lấy tham số từ URL (Query Parameters) [cite: 144-148]
    # Ví dụ: /api/v2/films?page=1&limit=5
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    start = (page - 1) * limit
    end = start + limit
    paginated_data = films_db[start:end]

    return jsonify({
        "status": "success",
        "version": "v2",
        "data": paginated_data,
        "meta": {
            "page": page,
            "limit": limit,
            "total_records": len(films_db)
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)