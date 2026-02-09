# Use standard Python base image (slim for smaller size)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port Render uses (dynamic via $PORT)
EXPOSE ${PORT:-8080}

# Start command: Use Gunicorn, bind to 0.0.0.0 and Render's $PORT
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-8080}", "app:app"]

