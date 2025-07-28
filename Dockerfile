FROM python:3.10-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Streamlit will run on
EXPOSE 3000

# Launch Streamlit on 0.0.0.0:3000
CMD ["streamlit", "run", "app/main.py", "--server.port", "3000", "--server.address", "0.0.0.0"]
