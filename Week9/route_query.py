# route_query.py
from flask import Blueprint, request, jsonify
from data import users_v1, users_v2

query_bp = Blueprint('query_versioning', __name__)

@query_bp.route('/api/users/by-query', methods=['GET'])
def get_users_query():
    # Lấy param 'version' từ URL, mặc định là '1'
    version = request.args.get('version', '1') 
    
    if version == '1':
        return jsonify({"data": users_v1, "warning": "Version 1 sắp bị loại bỏ."})
    elif version == '2':
        return jsonify({"data": users_v2})
    else:
        return jsonify({"error": f"Không hỗ trợ version {version}"}), 400