# route_header.py
from flask import Blueprint, request, jsonify
from data import users_v1, users_v2

header_bp = Blueprint('header_versioning', __name__)

@header_bp.route('/api/users/by-header', methods=['GET'])
def get_users_header():
    # Lấy version từ custom Header X-API-Version
    version = request.headers.get('X-API-Version', '1')
    
    if version == '1':
        return jsonify({"data": users_v1, "warning": "Đang dùng v1. Hãy cập nhật Header X-API-Version thành 2."})
    elif version == '2':
        return jsonify({"data": users_v2})
    else:
        return jsonify({"error": f"Không hỗ trợ version {version}"}), 400