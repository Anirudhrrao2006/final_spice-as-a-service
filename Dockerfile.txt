# Base Python image
FROM python:3.11-slim

# Install ngspice
RUN apt-get update && \
    apt-get install -y ngspice && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY simulator.py .

# Expose FastAPI port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "simulator:app", "--host", "0.0.0.0", "--port", "8000"]