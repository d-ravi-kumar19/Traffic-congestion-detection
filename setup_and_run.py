# setup_and_run.py
import os
import subprocess
from dotenv import load_dotenv
from app.utils.aws_util import download_model_from_s3

load_dotenv()  # Load environment variables

# Retrieve S3 environment variables
bucket_name = os.getenv("BUCKET_NAME")
model_file_name = os.getenv("MODEL_FILE_NAME")
local_model_path = os.getenv("LOCAL_MODEL_PATH")

def setup_model():
    try:
        # Ensure the target directory exists
        directory = os.path.dirname(local_model_path)
        os.makedirs(directory, exist_ok=True)

        # Check if the model file already exists and has size > 0
        if os.path.exists(local_model_path) and os.path.getsize(local_model_path) > 0:
            print(f"Model already exists at {local_model_path} and is valid. Exiting setup.")
            return  # Exit setup_model and allow run_app to proceed
        
        # Validate environment variables
        if not all([bucket_name, model_file_name, local_model_path]):
            raise ValueError("One or more environment variables are missing.")
        
        # Download model from S3
        download_model_from_s3(bucket_name, model_file_name, local_model_path)
        
        # Check if the model file exists after download
        if not os.path.exists(local_model_path):
            raise FileNotFoundError(f"Model weights file '{local_model_path}' not found after download.")
        
        # Verify that the downloaded model file has size > 0
        if os.path.getsize(local_model_path) == 0:
            raise ValueError(f"Model weights file '{local_model_path}' is empty after download.")
        
        print(f"Model successfully downloaded to {local_model_path}.")
        
    except Exception as e:
        print(f"Error during model setup: {e}")
        exit(1)  # Exit the script with an error code

def run_app():
    # Run the main FastAPI application
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    setup_model()
    run_app()
