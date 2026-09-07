FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers
RUN playwright install chromium

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the MCP server
CMD ["python", "server.py"]
