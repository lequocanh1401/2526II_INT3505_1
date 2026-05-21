from flask import Flask, jsonify, request

app = Flask(__name__)

# Đây chính là Endpoint Webhook (địa chỉ nhận tin tự động)
@app.route('/my-webhook-receiver', methods=['POST'])
def receive_webhook():
    payload = request.json
    print("\n[CLIENT] ĐÃ NHẬN ĐƯỢC WEBHOOK TỪ SERVER!")
    print(f"[CLIENT] Loại sự kiện: {payload.get('event')}")
    print(f"[CLIENT] Dữ liệu nhận được: {payload.get('payload')}")
    
    # Xử lý logic nghiệp vụ tại đây (ví dụ: cập nhật trạng thái giao hàng ở Frontend, gửi email cho khách...)
    
    # Bắt buộc trả về HTTP 200/204 để báo cho Server biết là đã nhận thành công, tránh việc Server retry lại
    return jsonify({"status": "Received"}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)