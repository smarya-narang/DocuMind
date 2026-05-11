# Use a lightweight version of Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the frontend code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
