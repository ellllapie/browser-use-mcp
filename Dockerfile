FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install uv (browser-use needs uvx command)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install browser-use CLI and browser
RUN uvx browser-use install

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the MCP server
CMD ["python", "server.py"]
