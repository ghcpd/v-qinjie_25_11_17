FROM python:3.11-slim

LABEL maintainer="Security Test Framework" \
      description="Reproducible environment for security vulnerability detection testing"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy test framework
COPY . .

# Create reports directory
RUN mkdir -p reports

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command runs the test suite
CMD ["python3", "test_runner.py"]
