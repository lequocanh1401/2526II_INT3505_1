# app.py
from flask import Flask

# Import các module Blueprint từ các file riêng lẻ
from route_url import url_bp
from route_query import query_bp
from route_header import header_bp

app = Flask(__name__)

# Đăng ký các module vào app chính
app.register_blueprint(url_bp)
app.register_blueprint(query_bp)
app.register_blueprint(header_bp)

if __name__ == '__main__':
    print("🚀 Server đang chạy tại http://127.0.0.1:5000")
    print("Các file đã được chia module thành công!")
    app.run(debug=True)