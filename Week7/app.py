from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Kết nối MongoDB (sử dụng localhost mặc định cổng 27017)
# Đảm bảo bạn đã cài đặt và bật MongoDB Compass/Server trên máy
client = MongoClient("mongodb://localhost:27017/")
db = client["soa_week7"]       # Tên database
products_col = db["products"]  # Tên collection

# 1. CREATE - Thêm sản phẩm (POST /products)
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Thiếu thông tin name hoặc price"}), 400
    
    new_product = {
        "name": data['name'],
        "price": data['price']
    }
    result = products_col.insert_one(new_product)
    return jsonify({"message": "Tạo thành công", "id": str(result.inserted_id)}), 201

# 2. READ ALL - Lấy danh sách (GET /products)
@app.route('/products', methods=['GET'])
def get_products():
    products = []
    for p in products_col.find():
        products.append({
            "id": str(p["_id"]),
            "name": p["name"],
            "price": p["price"]
        })
    return jsonify(products), 200

# 3. READ ONE - Lấy chi tiết 1 sản phẩm (GET /products/{id})
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    try:
        product = products_col.find_one({"_id": ObjectId(id)})
        if product:
            return jsonify({
                "id": str(product["_id"]),
                "name": product["name"],
                "price": product["price"]
            }), 200
        return jsonify({"error": "Không tìm thấy sản phẩm"}), 404
    except:
        return jsonify({"error": "ID không hợp lệ"}), 400

# 4. UPDATE - Cập nhật sản phẩm (PUT /products/{id})
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    try:
        result = products_col.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": data.get("name"), "price": data.get("price")}}
        )
        if result.matched_count:
            return jsonify({"message": "Cập nhật thành công"}), 200
        return jsonify({"error": "Không tìm thấy sản phẩm"}), 404
    except:
        return jsonify({"error": "ID không hợp lệ hoặc lỗi dữ liệu"}), 400

# 5. DELETE - Xóa sản phẩm (DELETE /products/{id})
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        result = products_col.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Xóa thành công"}), 200
        return jsonify({"error": "Không tìm thấy sản phẩm"}), 404
    except:
        return jsonify({"error": "ID không hợp lệ"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)