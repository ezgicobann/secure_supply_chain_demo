### 📌 Proje Hakkında  
Bu proje, yazılım tedarik zinciri güvenliğini (Software Supply Chain Security) sağlamak amacıyla geliştirilmiş uçtan uca bir DevSecOps otomasyonudur.  
Modern siber saldırıların (örn. SolarWinds, Log4j) hedefi haline gelen yazılım dağıtım süreçlerini güvence altına almak için tasarlanmıştır.  
Proje, geliştirilen Docker imajlarını GitHub Actions üzerinde otomatik olarak derler, Cosign (Sigstore) kullanarak kriptografik olarak imzalar ve son kullanıcı tarafında Python tabanlı bir araç ile bu imzaları doğrular.  
## Temel Amaçlar:  
Bütünlük (Integrity): İmajın üretimden dağıtıma kadar değiştirilmediğini garanti etmek.  
Kaynak Doğrulama (Authenticity): Yazılımın gerçekten yetkili CI/CD hattından çıktığını kanıtlamak.  
Otomasyon: İnsan hatasından arındırılmış güvenli bir dağıtım boru hattı (Pipeline) kurmak.  
## Sistem Mimarisi  
Sistem, aşağıdaki veri akışını izler:  
Geliştirici: Kodu main dalına gönderir (git push).  
GitHub Actions: CI/CD süreci tetiklenir,  
Docker imajı oluşturulur.  
İmzalama (Cosign): GitHub Secrets içinde saklanan Private Key ile imaj imzalanır.  
Kayıt (Registry): İmzalı imaj ve imza katmanı GitHub Container Registry (GHCR)'ye yüklenir.  
Doğrulama: İstemci, Public Key kullanarak imajı doğrular ve politikaya uygunsa çalıştırır.  
## Kurulum ve Kullanım  
Projeyi yerel ortamınızda çalıştırmak ve test etmek için aşağıdaki adımları izleyin.  
1. Gereksinimler  
Python 3.9+  
Docker Desktop  
Git2 .   
Projeyi Klonlayın  
Bash  
git clone https://github.com/ezgicobann/secure_supply_chain_demo.git  
cd secure_supply_chain_demo  
3. Bağımlılıkları Yükleyin  
Bash  
pip install -r requirements.txt  
Doğrulama Aracı (Verification Tool)  
Bu proje, imajların güvenliğini kontrol etmek için özel bir Python scripti içerir.  
## Kullanım:  
Bash  
python src/verify.py <IMAJ_ADRESI>  
Örnekler: Başarılı Senaryo (Kendi İmajınız):Bashpython src/verify.py ghcr.io/kullanici_adiniz/secure_supply_chain_demo:latest  
#### Çıktı: İmza doğrulama BAŞARILI ✅  
❌ Başarısız Senaryo (İmzasız/Sahte İmaj):Bashpython src/verify.py python:3.9-slim 
#### Çıktı: İmza doğrulama BAŞARISIZ! ❌ (Hata: No signature found) 
### Test Otomasyonu  
Projenin güvenilirliği  
Pytest ile yazılan birim testleri (Unit Tests) ile kanıtlanmıştır. 
5 farklı senaryo (başarılı imza, hatalı imza, politika ihlali vb.) test edilmektedir.  
Testleri çalıştırmak için:  
Bash  
python -m pytest  
Beklenen Çıktı:  
Plaintexttests/test_verify.py .....  [100%]  
5 passed in 0.12s  
### Kullanılan Teknolojiler  
Python: Doğrulama scripti ve test senaryoları  
Docker: Uygulama konteynırlaştırma  
GitHub Actions: CI/CD Otomasyonu  
Cosign (Sigstore): Konteynır imzalama ve doğrulama  
Pytest: Test otomasyonu  
  
📂 Proje Yapısı  
  
secure_supply_chain_demo/  
├── .github/workflows/   # CI/CD Pipeline (ci.yml)  
├── src/  
│   ├── app.py           # Örnek Uygulama  
│   └── verify.py        # Doğrulama Aracı (Core Logic)  
├── tests/  
│   └── test_verify.py   # Birim Testler  
├── cosign.pub           # Public Key (Doğrulama için)  
├── Dockerfile           # Konteynır Tanımı  
├── requirements.txt     # Python Kütüphaneleri  
└── README.md            # Proje Dokümantasyonu  
  
  
Geliştirici: Ezgi Çoban
