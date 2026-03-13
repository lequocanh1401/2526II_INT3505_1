from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__, static_folder='static')

# Khóa bí mật dùng để "ký" (sign) token. CHỈ SERVER ĐƯỢC BIẾT KHÓA NÀY.
app.config['SECRET_KEY'] = 'UET-SUPER-SECRET-KEY' 

books = [{"id": 1, "title": "Python UET", "author": "UET"}]

@app.route('/')
def home(): 
    return app.send_static_file('index.html')

# 1. API Đăng nhập: Cấp phát JWT
@app.route('/api/login', methods=['POST'])
def login():
    # Thực tế bạn sẽ kiểm tra user/pass ở đây. Để demo, ta cấp luôn token.
    # Tạo payload (dữ liệu chứa trong token)
    payload = {
        'user_id': 123,
        'role': 'sinhvien',
        # Token sẽ hết hạn sau 30 phút (đảm bảo tính bảo mật)
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) 
    }
    
    # Mã hóa thành JWT chuẩn
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

# 2. API Tài nguyên: Xác thực JWT
@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    auth_header = request.headers.get('Authorization')
    
    # Chuẩn xác thực bằng token thường có tiền tố 'Bearer '
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized - Thiếu hoặc sai định dạng Token!"}), 401

    # Cắt bỏ chữ 'Bearer ' để lấy chuỗi token thật
    token = auth_header.split(" ")[1]

    try:
        # Giải mã token. Thư viện sẽ tự động kiểm tra chữ ký và hạn sử dụng (exp)
        decoded_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        # Bạn có thể dùng decoded_data['user_id'] để biết ai đang gọi API
        
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Unauthorized - Token đã hết hạn!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Unauthorized - Token không hợp lệ bị chỉnh sửa!"}), 401

    # Nếu token hợp lệ, xử lý bình thường
    if request.method == 'GET':
        return jsonify(books)
    
    if request.method == 'POST':
        new_book = request.json
        books.append(new_book)
        return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug=True)