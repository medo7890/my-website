from flask import Flask, request, jsonify, send_from_directory
import os, html, requests

app = Flask(__name__, static_folder='.')

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json() or {}
    group = html.escape(data.get('groupLink','-'))
    method = html.escape(data.get('paymentMethod','-'))
    detail = html.escape(data.get('paymentDetail','-'))
    notes = html.escape(data.get('notes',''))
    msg = f"🔗 <b>رابط الجروب:</b> {group}\n💳 <b>وسيلة الدفع:</b> {method} - {detail}\n📝 <b>ملاحظات:</b> {notes}"
    send_telegram_message(msg)
    return jsonify({"ok":True})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
