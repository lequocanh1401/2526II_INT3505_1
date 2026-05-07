# route_url.py
from flask import Blueprint, jsonify, make_response
from data import users_v1, users_v2

# Khởi tạo Blueprint
url_bp = Blueprint('url_versioning', __name__)

# Endpoint v1 (Sắp bị loại bỏ)
@url_bp.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    response = make_response(jsonify({
        "data": users_v1,
        "meta": {
            "status": "deprecated",
            "message": "CẢNH BÁO: API v1 đã bị deprecate và sẽ bị xóa vào 31/12/2026. Vui lòng chuyển sang dùng /api/v2/users."
        }
    }))
    # Header báo hiệu API sắp "chết"
    response.headers['Deprecation'] = 'true'
    return response

# Endpoint v2 (Mới)
@url_bp.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    return jsonify({
        "data": users_v2,
        "meta": {"status": "active"}
    })