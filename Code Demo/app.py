from flask import Flask, jsonify, request, make_response 

app = Flask(__name__, static_folder='static')
books = [{"id": 1, "title": "Python UET", "author": "UET"}]

@app.route('/')
def home(): return app.send_static_file('index.html')

@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    token = request.headers.get('Authorization')
    if token != 'UET-SECRET-KEY':
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        res = make_response(jsonify(books))
        res.headers['Cache-Control'] = 'public, max-age=60' 
        return res
    
    if request.method == 'POST':
        new_book = request.json
        books.append(new_book)
        return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug=True)