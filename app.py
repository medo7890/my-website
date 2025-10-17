from flask import Flask, request, jsonify, send_from_directory
import os, html, requests

app = Flask(__name__, static_folder='.')

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    """دالة لإرسال رسالة إلى تيليجرام API."""
    # 💡 التحقق من وجود المتغيرات قبل الاستخدام
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        # إذا لم يتم العثور على المتغيرات، قم بإثارة خطأ واضح
        raise ValueError("TELEGRAM_TOKEN أو TELEGRAM_CHAT_ID غير موجود في المتغيرات البيئية.")
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    
    # التحقق من حالة الرد (إذا كان التوكن خطأ، ستفشل هنا)
    r.raise_for_status()
    return r.json()

@app.route('/send', methods=['POST'])
def send():
    """نقطة نهاية لاستقبال البيانات."""
    try:
        # ... (باقي كود استخلاص البيانات) ...
        data = request.get_json() or {}
        group = html.escape(data.get('groupLink','-'))
        method = html.escape(data.get('paymentMethod','-'))
        detail = html.escape(data.get('paymentDetail','-'))
        notes = html.escape(data.get('notes',''))
        
        msg = f"🔗 <b>رابط الجروب:</b> {group}\n💳 <b>وسيلة الدفع:</b> {method} - {detail}\n📝 <b>ملاحظات:</b> {notes}"
        
        send_telegram_message(msg)
        return jsonify({"ok":True})
        
    except ValueError as e:
        # رسالة خطأ واضحة إذا كانت المتغيرات مفقودة
        return jsonify({"ok": False, "error": str(e)}), 500
    except requests.exceptions.RequestException as e:
        # رسالة خطأ إذا كان هناك مشكلة في توكن أو API تيليجرام
        print(f"Telegram API Error: {e}")
        return jsonify({"ok": False, "error": "خطأ في الاتصال بتيليجرام. تحقق من التوكن ومعرّف الدردشة."}), 500
    except Exception as e:
        # للتعامل مع أي خطأ آخر
        return jsonify({"ok": False, "error": "حدث خطأ غير متوقع."}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    # تأكد من استخدام منفذ متغير
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
