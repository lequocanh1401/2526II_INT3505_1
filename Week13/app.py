from flask import Flask, request, jsonify, abort
import time

app = Flask(__name__)

# ==========================================
# 1. DATABASE GIẢ LẬP (Mô phỏng hệ thống)
# ==========================================
# Giả lập danh sách Developer đã đăng ký sản phẩm API này
DEVELOPERS = {
    "dev_pro_01": {"name": "Anh Le", "tier": "premium", "request_count": 0},
    "dev_free_02": {"name": "Nguyen Van A", "tier": "free", "request_count": 0}
}

# Giới hạn của từng gói dịch vụ (Monetization)
TIER_LIMITS = {
    "free": 3,      # Gói miễn phí: tối đa 3 requests
    "premium": 100  # Gói trả phí: tối đa 100 requests
}

# Hệ thống lưu trữ chỉ số đo lường (Analytics & KPIs)
KPIs = {
    "total_calls": 0,
    "error_calls": 0,
    "registered_developers": len(DEVELOPERS)
}

# ==========================================
# 2. CORE SERVICE (Sản phẩm API bán cho khách hàng)
# ==========================================
@app.route('/api/v1/data', methods=['GET'])
def get_premium_data():
    """
    API cung cấp dịch vụ dữ liệu. Khách hàng phải truyền API Key qua Header.
    """
    KPIs["total_calls"] += 1
    api_key = request.headers.get("X-API-KEY")

    # --- DEVELOPER EXPERIENCE (DX): Kiểm tra tính hợp lệ ---
    if not api_key or api_key not in DEVELOPERS:
        KPIs["error_calls"] += 1
        # Trả về lỗi rõ ràng, cấu trúc JSON tường minh giúp Developer dễ debug (Good DX)
        return jsonify({
            "error": "Unauthorized",
            "message": "API Key invalid or missing. Please check 'X-API-KEY' header."
        }), 401

    developer = DEVELOPERS[api_key]
    tier = developer["tier"]
    limit = TIER_LIMITS[tier]

    # --- MONETIZATION: Kiểm tra giới hạn gói cước (Rate Limiting) ---
    if developer["request_count"] >= limit:
        KPIs["error_calls"] += 1
        return jsonify({
            "error": "Quota Exceeded",
            "message": f"Your '{tier}' tier limit of {limit} requests has been reached. Please upgrade."
        }), 429

    # Tăng lượt sử dụng của Developer và xử lý logic thành công
    developer["request_count"] += 1
    
    return jsonify({
        "status": "success",
        "developer": developer["name"],
        "tier_used": tier,
        "remaining_requests": limit - developer["request_count"],
        "data": "Đây là dữ liệu giá trị cao từ sản phẩm API của bạn!"
    }), 200


# ==========================================
# 3. ANALYTICS DASHBOARD (Dành cho Quản trị viên sản phẩm)
# ==========================================
@app.route('/admin/analytics', methods=['GET'])
def get_analytics():
    """
    API nội bộ giúp Product Manager theo dõi các chỉ số KPIs của API Product.
    """
    total = KPIs["total_calls"]
    errors = KPIs["error_calls"]
    
    # Tính toán Error Rate tránh lỗi chia cho 0
    error_rate = f"{(errors / total) * 100:.2f}%" if total > 0 else "0.00%"

    return jsonify({
        "kpis": {
            "registered_developers_count": KPIs["registered_developers"], # Số lượng dev đăng ký
            "total_call_volume": total,                                  # Call volume
            "total_error_calls": errors,
            "error_rate": error_rate                                      # Error rate
        },
        "developer_usage_detail": DEVELOPERS
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)