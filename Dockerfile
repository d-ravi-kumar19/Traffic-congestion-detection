# Use TensorFlow's official Docker image with Python pre-installed
FROM tensorflow/tensorflow:2.13.0  

# Set the working directory to /code
WORKDIR /code

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to /code
COPY . /code

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start FastAPI app with Uvicorn (path updated to /code/main:app)
CMD ["python", "setup_and_run.py"]
