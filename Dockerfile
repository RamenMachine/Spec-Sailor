# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api ./api
COPY data ./data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Start command
CMD uvicorn api.simple_api:app --host 0.0.0.0 --port ${PORT:-8000}
