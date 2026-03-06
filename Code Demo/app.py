from flask import Flask, jsonify, request

app = Flask(__name__, static_folder='static')
books = [{"id": 1, "title": "Python UET", "author": "UET"}]

@app.route('/')
def home(): return app.send_static_file('index.html')

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    token = request.headers.get('Authorization')
    if token != 'UET-SECRET-KEY':
        return jsonify({"error": "Unauthorized - Phải có Token mới cho xem!"}), 401

    if request.method == 'GET':
        return jsonify(books)
    
    if request.method == 'POST':
        new_book = request.json
        books.append(new_book)
        return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug=True)