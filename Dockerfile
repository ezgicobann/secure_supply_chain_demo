# Hafif bir Python imajı kullanıyoruz
FROM python:3.9-slim

WORKDIR /app

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY src/ src/

# Güvenlik için root olmayan kullanıcı (Best Practice)
RUN useradd -m appuser
USER appuser

EXPOSE 5000

CMD ["python", "src/app.py"]