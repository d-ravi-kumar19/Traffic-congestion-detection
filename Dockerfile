# Base image with Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 9000 for Flask
EXPOSE 9000

# Start the Flask app
CMD ["python", "main.py"]
