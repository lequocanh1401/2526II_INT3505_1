from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập database bằng bộ nhớ tạm (In-memory Data)
ITEMS = [
    {"id": 1, "name": "Pizza Hải Sản", "price": 120000, "status": "available"},
    {"id": 2, "name": "Burger Bò", "price": 65000, "status": "available"},
    {"id": 3, "name": "Gà Rán", "price": 45000, "status": "out_of_stock"},
    {"id": 4, "name": "Mì Ý Sốt Bò Băm", "price": 90000, "status": "available"},
]

# 1. QUERY PATTERN: Minh họa Filtering (lọc theo status) và Pagination (phân trang)
@app.route('/api/items', methods=['GET'])
def get_items():
    status_filter = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 2))
    
    # Filtering
    filtered_items = ITEMS
    if status_filter:
        filtered_items = [item for item in ITEMS if item['status'] == status_filter]
        
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = filtered_items[start_idx:end_idx]
    
    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(filtered_items),
        "data": paginated_items
    })

# 2. CRUD & HATEOAS PATTERN: Lấy chi tiết tài nguyên và trả về các "Hành động tiếp theo"
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item_detail(item_id):
    item = next((item for item in ITEMS if item['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
        
    # HATEOAS: Trả về dữ liệu kèm các liên kết trạng thái ứng dụng có thể thực hiện tiếp
    return jsonify({
        "data": item,
        "_links": {
            "self": {"href": f"/api/items/{item_id}", "method": "GET"},
            "update": {"href": f"/api/items/{item_id}", "method": "PUT"},
            "delete": {"href": f"/api/items/{item_id}", "method": "DELETE"},
            "all_items": {"href": "/api/items", "method": "GET"}
        }
    })

# 3. CRUD: Các thao tác Create, Update, Delete còn lại
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = {"id": len(ITEMS) + 1, "name": data['name'], "price": data['price'], "status": "available"}
    ITEMS.append(new_item)
    return jsonify({"message": "Created", "item": new_item}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in ITEMS if item['id'] == item_id), None)
    if item:
        item.update(request.json)
        return jsonify({"message": "Updated", "item": item})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global ITEMS
    ITEMS = [item for item in ITEMS if item['id'] != item_id]
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)