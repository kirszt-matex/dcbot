FROM python:3.11-slim

WORKDIR /app
COPY . .

# Tesseract OCR telepítése (ha használod)
RUN apt-get update && apt-get install -y tesseract-ocr

# Függőségek telepítése
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]