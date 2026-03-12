from flask import Flask, jsonify

app = Flask(__name__)

# Dữ liệu giả lập từ database 
films_db = [
    {"film_id": 1, "title": "Academy Dinosaur"},
    {"film_id": 2, "title": "Ace Goldfinger"}
]

# 1. Demo API Thành công: Lấy danh sách phim
@app.route('/api/v1/films', methods=['GET'])
def get_all_films():
    # Nhất quán: Luôn trả về cấu trúc status, message, data, meta
    response = {
        "status": "success",
        "message": "Lấy danh sách phim thành công",
        "data": films_db,
        "meta": {"page": 1, "total_pages": 1}
    }
    return jsonify(response), 200

# 2. Demo API Thất bại: Tìm phim không tồn tại
@app.route('/api/v1/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    # Giả lập không tìm thấy phim có ID = 999
    if film_id == 999:
        # Nhất quán: Dù lỗi vẫn phải giữ nguyên cấu trúc bộ khung như trên
        response = {
            "status": "error",
            "message": f"Không tìm thấy bộ phim với ID = {film_id}",
            "data": None,
            "meta": None
        }
        return jsonify(response), 404
    
    # Nếu tìm thấy (cho các ID khác)
    return jsonify({"status": "success", "data": {"film_id": film_id, "title": "Sample Film"}}), 200

if __name__ == '__main__':
    app.run(debug=True)