# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv pip install --system --no-cache .

# Copy credentials and application code
COPY credentials.json /app/credentials.json
COPY . .

# Expose the port
EXPOSE 8989

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989"]
