from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)

# Cấu hình Swagger UI
SWAGGER_URL = '/api/docs'  # Link truy cập Swagger UI lúc demo
API_URL = '/openapi.yaml'  # Link để Swagger UI đọc file YAML

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Tài liệu API Quản lý Sách"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

# Route để Flask cung cấp file YAML cho Swagger UI đọc
@app.route('/openapi.yaml')
def send_yaml():
    yaml_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(yaml_dir, 'openapi.yaml')

if __name__ == '__main__':
    app.run(debug=True)