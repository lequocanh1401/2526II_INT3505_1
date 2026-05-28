import threading
import time
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập danh sách các client đăng ký nhận Webhook khi có đơn hàng thành công
WEBHOOK_REGISTRATIONS = []

# API để Client vào "đăng ký" URL của họ
@app.route('/api/register-webhook', methods=['POST'])
def register_webhook():
    data = request.json
    client_url = data.get('target_url')
    if client_url and client_url not in WEBHOOK_REGISTRATIONS:
        WEBHOOK_REGISTRATIONS.append(client_url)
    return jsonify({"status": "Registered successfully", "total_subscribers": len(WEBHOOK_REGISTRATIONS)})

# Hàm giả lập gửi Webhook (chạy bất đồng bộ để tránh nghẽn luồng chính)
def trigger_webhook_event(order_data):
    time.sleep(2)  # Giả lập độ trễ xử lý thanh toán ngân hàng
    print(f"\n[SERVER] Sự kiện: Đơn hàng {order_data['order_id']} thành công! Bắt đầu phát Webhook...")
    
    for url in WEBHOOK_REGISTRATIONS:
        try:
            # Server chủ động gọi sang Client (Reverse API)
            requests.post(url, json={"event": "ORDER_COMPLETED", "payload": order_data}, timeout=5)
            print(f"[SERVER] Đã đẩy data thành công sang Client URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"[SERVER] Gửi thất bại sang {url}: {e}")

# API tạo đơn hàng - khi gọi API này, hệ thống sẽ tự động kích hoạt sự kiện để bắn Webhook
@app.route('/api/checkout', methods=['POST'])
def checkout():
    order_data = {"order_id": 999, "amount": 250000, "customer": "Lê Quốc Anh"}
    
    # Kích hoạt luồng gửi Webhook cho các bên đã đăng ký
    threading.Thread(target=trigger_webhook_event, args=(order_data,)).start()
    
    return jsonify({"message": "Order received. Processing payment..."}), 202

if __name__ == '__main__':
    app.run(port=5002, debug=True)