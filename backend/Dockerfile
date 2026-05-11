# Use a lightweight version of Python
FROM python:3.10-slim

# Set the folder inside the container
WORKDIR /app

# Copy requirements first (for speed)
COPY requirements.txt .

# Install the libraries
# We use --no-cache-dir to keep the file size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# The command to run the backend API
ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]