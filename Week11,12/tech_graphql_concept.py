from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập DB có quan hệ phức tạp: User có thông tin cá nhân và danh sách Đơn hàng
USER_DATABASE = {
    "profile": {"id": 101, "name": "Lê Quốc Anh", "email": "quocanh@uet.edu.vn", "role": "Student"},
    "orders": [
        {"order_id": 1, "product": "Laptop Dell", "price": 20000000},
        {"order_id": 2, "product": "Chuột không dây", "price": 3500}
    ]
}

# GraphQL đặc trưng bởi việc CHỈ CÓ 1 ENDPOINT DUY NHẤT và dùng POST
@app.route('/graphql', methods=['POST'])
def mock_graphql():
    req_data = request.json
    # Client gửi danh sách các trường (fields) họ thực sự cần
    # Ví dụ body: {"fields": ["profile.name", "orders.product"]}
    requested_fields = req_data.get("fields", [])
    
    response_data = {}
    
    # Server phân tích "đồ thị" yêu cầu và chỉ đóng gói đúng thứ client cần
    if "profile.name" in requested_fields:
        if "profile" not in response_data: response_data["profile"] = {}
        response_data["profile"]["name"] = USER_DATABASE["profile"]["name"]
        
    if "profile.email" in requested_fields:
        if "profile" not in response_data: response_data["profile"] = {}
        response_data["profile"]["email"] = USER_DATABASE["profile"]["email"]
        
    if "orders.product" in requested_fields:
        response_data["orders"] = [{"product": o["product"]} for o in USER_DATABASE["orders"]]
        
    if not requested_fields:
        # Nếu không truyền gì, mặc định trả toàn bộ (Tư duy của REST thông thường)
        response_data = USER_DATABASE

    return jsonify({"data": response_data})

if __name__ == '__main__':
    app.run(port=5004, debug=True)