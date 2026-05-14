import logging
import random
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import pybreaker

app = Flask(__name__)

# ==========================================
# 1. MONITORING: LOGS & METRICS
# ==========================================

# Thiết lập Logs: Ghi lại các hoạt động của hệ thống
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Thiết lập Metrics: Tự động expose endpoint /metrics cho Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Demo SOA Week 10', version='1.0.0')


# ==========================================
# 2. SECURITY: RATE LIMITING
# ==========================================

# Thiết lập giới hạn request dựa trên IP của client
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"] # Giới hạn mặc định cho toàn bộ app
)


# ==========================================
# 3. RESILIENCE: CIRCUIT BREAKER
# ==========================================

# Cấu hình Circuit Breaker: Thất bại 3 lần liên tiếp sẽ ngắt mạch (Mở). 
# Sau 10 giây sẽ cho phép thử lại (Half-Open).
db_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)

# Hàm giả lập gọi sang một External Service (hoặc Database) không ổn định
@db_breaker
def fetch_unstable_data():
    # Giả lập 70% cơ hội service bên ngoài bị lỗi
    if random.random() < 0.7: 
        logger.error("Lỗi: Gọi External Service thất bại!")
        raise Exception("Mất kết nối mạng!")
    
    logger.info("Thành công: Đã lấy được dữ liệu từ External Service.")
    return {"data": "Dữ liệu quan trọng từ Service khác"}


# ==========================================
# 4. API ENDPOINTS DEMO
# ==========================================

@app.route('/')
def index():
    logger.info("Truy cập trang chủ")
    return jsonify({"message": "Hệ thống đang hoạt động (API Gateway giả lập)"})

# Demo Rate Limiting: Giới hạn nghiêm ngặt hơn
@app.route('/api/fast')
@limiter.limit("3 per minute") # Chỉ cho phép 3 request / 1 phút
def fast_api():
    logger.info("Truy cập API bị giới hạn tốc độ")
    return jsonify({"message": "Gọi API thành công! API này chỉ gọi được 3 lần/phút."})

# Demo Circuit Breaker
@app.route('/api/external')
def external_api():
    try:
        data = fetch_unstable_data()
        return jsonify({"status": "success", "data": data})
    
    except pybreaker.CircuitBreakerError:
        # Lỗi này văng ra khi Mạch đang MỞ. Hệ thống chặn request ngay lập tức 
        # mà không cần tốn thời gian gọi đến hàm fetch_unstable_data nữa.
        logger.warning("CIRCUIT BREAKER ĐANG MỞ: Tạm ngưng request để bảo vệ hệ thống.")
        return jsonify({"error": "Service hiện không khả dụng, vui lòng thử lại sau 10 giây."}), 503
    
    except Exception as e:
        # Lỗi thông thường khi Mạch đang ĐÓNG nhưng request vẫn bị fail
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)