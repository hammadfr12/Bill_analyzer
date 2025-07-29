# Use a slim Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 3000

# Launch Streamlit
CMD ["streamlit", "run", "app/main.py", "--server.port", "3000", "--server.address", "0.0.0.0"]
