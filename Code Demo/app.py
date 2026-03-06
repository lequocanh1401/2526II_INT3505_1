from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/books')
def get_books():
    books = [
        {"id": 1, "title": "Lập trình Python", "author": "UET"},
        {"id": 2, "title": "Kiến trúc SOA", "author": "Thầy của bạn"},
    ]
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)