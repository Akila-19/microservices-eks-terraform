from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

USER_SERVICE = 'http://user-service:5000'
PRODUCT_SERVICE = 'http://product-service:5001'

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "api-gateway"}), 200

@app.route('/status', methods=['GET'])
def status():
    services_status = {}
    try:
        response = requests.get(f'{USER_SERVICE}/health', timeout=5)
        services_status['user-service'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        services_status['user-service'] = 'offline'
    try:
        response = requests.get(f'{PRODUCT_SERVICE}/health', timeout=5)
        services_status['product-service'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        services_status['product-service'] = 'offline'
    return jsonify({'gateway': 'healthy', 'services': services_status}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        response = requests.get(f'{USER_SERVICE}/users')
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'User service unavailable'}), 503

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        response = requests.get(f'{USER_SERVICE}/users/{user_id}')
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'User service unavailable'}), 503

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        response = requests.post(f'{USER_SERVICE}/users', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'User service unavailable'}), 503

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        response = requests.get(f'{PRODUCT_SERVICE}/products')
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'Product service unavailable'}), 503

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        response = requests.get(f'{PRODUCT_SERVICE}/products/{product_id}')
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'Product service unavailable'}), 503

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        response = requests.post(f'{PRODUCT_SERVICE}/products', json=request.get_json())
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({'error': 'Product service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


