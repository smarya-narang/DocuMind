# 1. Use a lightweight version of Python
FROM python:3.10-slim

# 2. Set the folder inside the container
WORKDIR /app

# 3. Copy requirements first (for speed)
COPY requirements.txt .

# 4. Install the libraries
# We use --no-cache-dir to keep the file size small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the backend code
COPY . .

# 6. The command to run your app
# (We point to the pipeline script we made in Week 2)
ENV PYTHONPATH=/app
CMD ["python", "app/services/pipeline.py"]