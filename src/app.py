import logging
import sys
from flask import Flask, jsonify

#Demo icin test
# Logging yapılandırması (Yönerge Md. 4)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    try:
        logger.info("Anasayfa isteği alındı.")
        return jsonify({"message": "Güvenli Tedarik Zinciri Demosu v1.0"}), 200
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        return jsonify({"error": "Sunucu hatası"}), 500

if __name__ == '__main__':
    logger.info("Uygulama başlatılıyor...")
    app.run(host='0.0.0.0', port=5000)