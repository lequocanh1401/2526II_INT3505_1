# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- PHẦN 1: Hàm logic (Dành cho Unit Test) ---
def calculate_total(price, quantity):
    """Hàm tính tổng tiền. Nếu nhập sai số âm thì trả về 0"""
    if price < 0 or quantity < 0:
        return 0
    return price * quantity

# --- PHẦN 2: API Endpoint (Dành cho Integration Test) ---
@app.route('/api/calculate', methods=['POST'])
def calculate_api():
    """Nhận HTTP Request, gọi hàm logic, và trả về HTTP Response"""
    data = request.get_json()
    
    # Lấy dữ liệu từ user, mặc định là 0 nếu không có
    price = data.get('price', 0)
    quantity = data.get('quantity', 0)
    
    # Gọi hàm tính toán
    total = calculate_total(price, quantity)
    
    # Trả về kết quả JSON
    return jsonify({"total": total, "status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)