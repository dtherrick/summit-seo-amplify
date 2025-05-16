# Use Python base image
FROM python:3.12-slim

# Set environment variable defaults
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV \
    LOG_LEVEL=INFO \
    PORT=8000 \
    WORKERS=4

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make scripts executable
RUN chmod +x scripts/start.sh scripts/validate_env.py

# Validate environment variables during build
RUN if [ "$NODE_ENV" = "production" ]; then \
        python scripts/validate_env.py --check-build; \
    else \
        python scripts/validate_env.py --check-build --dev; \
    fi

# Expose port
EXPOSE 8000

# Use the startup script as entrypoint
ENTRYPOINT ["/app/scripts/start.sh"]
