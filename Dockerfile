FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ngspice && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual script
COPY simulator.py .

# Use environment variables to ensure it listens on the port Render provides
ENV PORT=10000
CMD python -m uvicorn simulator:app --host 0.0.0.0 --port $PORT
