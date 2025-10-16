from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.get_json() or {}
        print("📨 Received data:", data)  # علشان نشوف في الـLogs
        return jsonify({"ok": True, "message": "تم الاستلام بنجاح"})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)