import subprocess
import logging
import json
import sys

# Yönerge Md. 16: Logging ve Hata Yönetimi
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageVerifier:
    def __init__(self, public_key_path="cosign.pub"):
        self.public_key_path = public_key_path

    def verify_signature(self, image_ref):
        """
        Cosign aracını kullanarak imaj imzasını doğrular.
        """
        logger.info(f"İmaj doğrulanıyor: {image_ref}")
        
        command = [
            "cosign", "verify",
            "--key", self.public_key_path,
            image_ref
        ]

        try:
            # Komutu çalıştır ve çıktıyı yakala
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info("İmza doğrulama BAŞARILI. ✅")
            return True, result.stdout
            
        except subprocess.CalledProcessError as e:
            logger.error(f"İmza doğrulama BAŞARISIZ! ❌ Hata: {e.stderr}")
            return False, e.stderr
        except Exception as e:
            logger.error(f"Beklenmedik hata: {str(e)}")
            return False, str(e)

    def check_policy(self, verification_output):
        """
        Yönerge Md. 3: Politika kontrolü.
        Doğrulama çıktısındaki verilerin (Issuer vb.) güvenilir olup olmadığını kontrol eder.
        """
        if not verification_output:
            return False

        # Cosign çıktısı JSON formatında satırlar içerebilir, biz basitçe metin kontrolü yapalım
        # Gerçek bir senaryoda JSON parse edilir.
        if "critical" in verification_output:
             # Örnek Politika: Kritik güvenlik açığı varsa reddet (Simülasyon)
            logger.warning("Politika Uyarısı: Kritik etiket bulundu.")
            return False
            
        logger.info("Politika kontrolü: GEÇERLİ.")
        return True

if __name__ == "__main__":
    # Test amaçlı kullanım: python src/verify.py <image_name>
    if len(sys.argv) > 1:
        verifier = ImageVerifier()
        is_valid, _ = verifier.verify_signature(sys.argv[1])
        if is_valid:
            sys.exit(0)
        else:
            sys.exit(1)