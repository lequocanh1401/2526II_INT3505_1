from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "UET_SOA_KEY"

# Database giả lập lưu Refresh Token
refresh_tokens_db = {}

@app.route('/login', methods=['POST'])
def login():
    # Demo ROLE và SCOPE trong JWT
    user_payload = {
        "user_id": 1,
        "role": "student",              # ROLE
        "scopes": ["read", "write"],     # SCOPES
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30) # Access token sống 30s
    }
    access_token = jwt.encode(user_payload, SECRET_KEY, algorithm="HS256")
    
    # REFRESH TOKEN: Chuỗi ngẫu nhiên, sống lâu hơn
    refresh_token = "refresh_token_xyz_123"
    refresh_tokens_db[1] = refresh_token
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer" # BEARER TOKEN
    })

@app.route('/refresh', methods=['POST'])
def refresh():
    # Demo dùng Refresh Token để lấy Access Token mới
    r_token = request.json.get('refresh_token')
    if r_token == refresh_tokens_db.get(1):
        new_payload = {
            "user_id": 1,
            "role": "student",
            "scopes": ["read", "write"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        return jsonify({"access_token": jwt.encode(new_payload, SECRET_KEY)})
    return jsonify({"msg": "Refresh Token không khớp!"}), 403

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header: return jsonify({"msg": "No Token"}), 401
    
    token = auth_header.split(" ")[1] # Cắt bỏ chữ 'Bearer '
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"msg": "Vào được rồi!", "data": data})
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Token hết hạn! Hãy gọi /refresh"}), 401

if __name__ == '__main__':
    print("Server đang chạy tại http://127.0.0.1:5000") # Dòng này để kiểm tra xem nó có chạy không
    app.run(debug=True)