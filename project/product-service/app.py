from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

products = [
    {"id": "1", "name": "Laptop", "price": 999.99, "stock": 50, "created_at": "2024-01-01T00:00:00"},
    {"id": "2", "name": "Mouse", "price": 29.99, "stock": 200, "created_at": "2024-01-02T00:00:00"},
    {"id": "3", "name": "Keyboard", "price": 79.99, "stock": 150, "created_at": "2024-01-03T00:00:00"}
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "product-service"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products, "count": len(products)}), 200

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Name and price are required"}), 400
    product = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "price": float(data['price']),
        "stock": data.get('stock', 0),
        "created_at": datetime.utcnow().isoformat()
    }
    products.append(product)
    return jsonify(product), 201

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    if 'name' in data:
        product['name'] = data['name']
    if 'price' in data:
        product['price'] = float(data['price'])
    if 'stock' in data:
        product['stock'] = int(data['stock'])
    return jsonify(product), 200

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

