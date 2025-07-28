# 1. Use a lightweight Python base
FROM python:3.10-slim

# 2. Install system deps for PDF→image & OCR
RUN apt-get update 
 && apt-get install -y --no-install-recommends 
      poppler-utils 
      tesseract-ocr 
      libgl1 
 && rm -rf /var/lib/apt/lists/*

# 3. Set working directory
WORKDIR /app

# 4. Copy project files
COPY . .

# 5. Install Python dependencies
RUN pip install --upgrade pip 
 && pip install -r requirements.txt

# 6. Expose Streamlit port
EXPOSE 8501

# 7. Launch Streamlit
CMD ["streamlit", "run", "app/main.py", "--server.port", "8501", "--server.enableCORS=false"]
