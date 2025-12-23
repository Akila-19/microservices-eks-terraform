from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

users = [
    {"id": "1", "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01T00:00:00"},
    {"id": "2", "name": "Jane Smith", "email": "jane@example.com", "created_at": "2024-01-02T00:00:00"}
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "user-service"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": users, "count": len(users)}), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    user = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "email": data['email'],
        "created_at": datetime.utcnow().isoformat()
    }
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)