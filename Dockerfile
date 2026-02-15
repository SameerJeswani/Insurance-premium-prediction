# Use Python 3.11 base image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

# Expose port (optional but fine)
EXPOSE 8000

# Start FastAPI using Render PORT
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
