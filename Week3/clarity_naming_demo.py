from flask import Flask, jsonify, request

app = Flask(__name__)

# --- NHÓM 1: THIẾT KẾ TỒI (BAD PRACTICES) ---
# Lỗi: Dùng động từ, CamelCase, sai HTTP Method
@app.route('/getAllFilms', methods=['GET'])
def get_films_bad():
    return jsonify({"message": "Dùng động từ 'getAll' và CamelCase là sai chuẩn"}), 200

@app.route('/update_Film', methods=['POST'])
def update_film_bad():
    return jsonify({"message": "Dùng POST để update và dùng dấu gạch dưới '_' là không nên"}), 200


# --- NHÓM 2: THIẾT KẾ CHUẨN (BEST PRACTICES) ---
# 1. Dùng danh từ số nhiều, chữ thường, dấu gạch ngang [cite: 70-72, 93, 104]
# 2. Hành động được thể hiện qua HTTP Method (GET, PUT, DELETE) [cite: 82-91]
@app.route('/films', methods=['GET'])
def get_films_good():
    return jsonify({"message": "Chuẩn: Danh từ số nhiều, GET để lấy danh sách"}), 200

@app.route('/films/<int:id>', methods=['PUT'])
def update_film_good(id):
    return jsonify({"message": f"Chuẩn: PUT dùng để cập nhật tài nguyên {id}"}), 200

# 3. Demo Nesting: Thể hiện quan hệ cha-con (Ví dụ: Các bản thuê của 1 khách hàng) [cite: 120-124]
@app.route('/customers/<int:id>/rentals', methods=['GET'])
def get_customer_rentals(id):
    return jsonify({"message": f"Chuẩn: Nesting thể hiện rentals thuộc về customer {id}"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Chạy port 5001 để tránh trùng